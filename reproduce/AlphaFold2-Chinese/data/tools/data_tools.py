# Copyright 2021 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
'''data tools'''
import glob
import os
import subprocess
import contextlib
import shutil
import tempfile
import time

from typing import Any, Mapping, Optional, Sequence

from absl import logging

_HHBLITS_DEFAULT_P = 20
_HHBLITS_DEFAULT_Z = 500


def _to_a3m(sequences: Sequence[str]) -> str:
    """Converts sequences to an a3m file."""
    names = ['sequence %d' % i for i in range(1, len(sequences) + 1)]
    a3m = []
    for sequence, name in zip(sequences, names):
        a3m.append(u'>' + name + u'\n')
        a3m.append(sequence + u'\n')
    return ''.join(a3m)


class Kalign:
    """Python wrapper of the Kalign binary."""

    def __init__(self, *, binary_path: str):
        """Initializes the Python Kalign wrapper.

        Args:
          binary_path: The path to the Kalign binary.
        """
        self.binary_path = binary_path

    def align(self, sequences: Sequence[str]) -> str:
        """Aligns the sequences and returns the alignment in A3M string.

        Args:
          sequences: A list of query sequence strings. The sequences have to be at
            least 6 residues long (Kalign requires this). Note that the order in
            which you give the sequences might alter the output slightly as
            different alignment tree might get constructed.

        Returns:
          A string with the alignment in a3m format.

        Raises:
          RuntimeError: If Kalign fails.
          ValueError: If any of the sequences is less than 6 residues long.
        """
        logging.info('Aligning %d sequences', len(sequences))

        for s in sequences:
            if len(s) < 6:
                raise ValueError('Kalign requires all sequences to be at least 6 '
                                 'residues long. Got %s (%d residues).' % (s, len(s)))

        with tmpdir_manager(base_dir='/tmp') as query_tmp_dir:
            input_fasta_path = os.path.join(query_tmp_dir, 'input.fasta')
            output_a3m_path = os.path.join(query_tmp_dir, 'output.a3m')

            with open(input_fasta_path, 'w') as f:
                f.write(_to_a3m(sequences))

            cmd = [self.binary_path, '-i', input_fasta_path, '-o', output_a3m_path, '-format', 'fasta',]

            logging.info('Launching subprocess "%s"', ' '.join(cmd))
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            with timing('Kalign query'):
                stdout, stderr = process.communicate()
                retcode = process.wait()
                logging.info('Kalign stdout:\n%s\n\nstderr:\n%s\n', stdout.decode('utf-8'), stderr.decode('utf-8'))

            if retcode:
                raise RuntimeError(
                    'Kalign failed\nstdout:\n%s\n\nstderr:\n%s\n' % (stdout.decode('utf-8'), stderr.decode('utf-8')))

            with open(output_a3m_path) as f:
                a3m = f.read()

            return a3m


@contextlib.contextmanager
def tmpdir_manager(base_dir: Optional[str] = None):
    """Context manager that deletes a temporary directory on exit."""
    tmpdir = tempfile.mkdtemp(dir=base_dir)
    try:
        yield tmpdir
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


@contextlib.contextmanager
def timing(msg: str):
    logging.info('Started %s', msg)
    tic = time.time()
    yield
    toc = time.time()
    logging.info('Finished %s in %.3f seconds', msg, toc - tic)


class HHBlits:
    """Python wrapper of the HHblits binary."""

    def __init__(self,
                 *,
                 binary_path: str,
                 databases: Sequence[str],
                 n_cpu: int = 4,
                 n_iter: int = 3,
                 e_value: float = 0.001,
                 maxseq: int = 1_000_000,
                 realign_max: int = 100_000,
                 maxfilt: int = 100_000,
                 min_prefilter_hits: int = 1000,
                 all_seqs: bool = False,
                 alt: Optional[int] = None,
                 p: int = _HHBLITS_DEFAULT_P,
                 z: int = _HHBLITS_DEFAULT_Z):
        """Initializes the Python HHblits wrapper.

        Args:
          binary_path: The path to the HHblits executable.
          databases: A sequence of HHblits database paths. This should be the
            common prefix for the database files (i.e. up to but not including
            _hhm.ffindex etc.)
          n_cpu: The number of CPUs to give HHblits.
          n_iter: The number of HHblits iterations.
          e_value: The E-value, see HHblits docs for more details.
          maxseq: The maximum number of rows in an input alignment. Note that this
            parameter is only supported in HHBlits version 3.1 and higher.
          realign_max: Max number of HMM-HMM hits to realign. HHblits default: 500.
          maxfilt: Max number of hits allowed to pass the 2nd prefilter.
            HHblits default: 20000.
          min_prefilter_hits: Min number of hits to pass prefilter.
            HHblits default: 100.
          all_seqs: Return all sequences in the MSA / Do not filter the result MSA.
            HHblits default: False.
          alt: Show up to this many alternative alignments.
          p: Minimum Prob for a hit to be included in the output hhr file.
            HHblits default: 20.
          z: Hard cap on number of hits reported in the hhr file.
            HHblits default: 500. NB: The relevant HHblits flag is -Z not -z.

        Raises:
          RuntimeError: If HHblits binary not found within the path.
        """
        self.binary_path = binary_path
        self.databases = databases

        for database_path in self.databases:
            if not glob.glob(database_path + '_*'):
                logging.error('Could not find HHBlits database %s', database_path)
                raise ValueError(f'Could not find HHBlits database {database_path}')

        self.n_cpu = n_cpu
        self.n_iter = n_iter
        self.e_value = e_value
        self.maxseq = maxseq
        self.realign_max = realign_max
        self.maxfilt = maxfilt
        self.min_prefilter_hits = min_prefilter_hits
        self.all_seqs = all_seqs
        self.alt = alt
        self.p = p
        self.z = z

    def query(self, input_fasta_path: str) -> Mapping[str, Any]:
        """Queries the database using HHblits."""
        with tmpdir_manager(base_dir='/tmp') as query_tmp_dir:
            a3m_path = os.path.join(query_tmp_dir, 'output.a3m')

            db_cmd = []
            for db_path in self.databases:
                db_cmd.append('-d')
                db_cmd.append(db_path)
            cmd = [
                self.binary_path,
                '-i', input_fasta_path,
                '-cpu', str(self.n_cpu),
                '-oa3m', a3m_path,
                '-o', '/dev/null',
                '-n', str(self.n_iter),
                '-e', str(self.e_value),
                '-maxseq', str(self.maxseq),
                '-realign_max', str(self.realign_max),
                '-maxfilt', str(self.maxfilt),
                '-min_prefilter_hits', str(self.min_prefilter_hits)]
            if self.all_seqs:
                cmd += ['-all']
            if self.alt:
                cmd += ['-alt', str(self.alt)]
            if self.p != _HHBLITS_DEFAULT_P:
                cmd += ['-p', str(self.p)]
            if self.z != _HHBLITS_DEFAULT_Z:
                cmd += ['-Z', str(self.z)]
            cmd += db_cmd

            logging.info('Launching subprocess "%s"', ' '.join(cmd))
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            with timing('HHblits query'):
                stdout, stderr = process.communicate()
                retcode = process.wait()

            if retcode:
                # Logs have a 15k character limit, so log HHblits error line by
                # line.
                logging.error('HHblits failed. HHblits stderr begin:')
                for error_line in stderr.decode('utf-8').splitlines():
                    if error_line.strip():
                        logging.error(error_line.strip())
                logging.error('HHblits stderr end')
                raise RuntimeError('HHblits failed\nstdout:\n%s\n\nstderr:\n%s\n' % (
                    stdout.decode('utf-8'), stderr[:500_000].decode('utf-8')))

            with open(a3m_path) as f:
                a3m = f.read()

        raw_output = dict(
            a3m=a3m,
            output=stdout,
            stderr=stderr,
            n_iter=self.n_iter,
            e_value=self.e_value)
        return raw_output


class HHSearch:
    """Python wrapper of the HHsearch binary."""

    def __init__(self,
                 *,
                 binary_path: str,
                 databases: Sequence[str],
                 maxseq: int = 1_000_000):
        """Initializes the Python HHsearch wrapper.

        Args:
          binary_path: The path to the HHsearch executable.
          databases: A sequence of HHsearch database paths. This should be the
            common prefix for the database files (i.e. up to but not including
            _hhm.ffindex etc.)
          maxseq: The maximum number of rows in an input alignment. Note that this
            parameter is only supported in HHBlits version 3.1 and higher.

        Raises:
          RuntimeError: If HHsearch binary not found within the path.
        """
        self.binary_path = binary_path
        self.databases = databases
        self.maxseq = maxseq

        for database_path in self.databases:
            if not glob.glob(database_path + '_*'):
                logging.error(
                    'Could not find HHsearch database %s',
                    database_path)
                raise ValueError(
                    f'Could not find HHsearch database {database_path}')

    def query(self, a3m: str) -> str:
        """Queries the database using HHsearch using a given a3m."""
        with tmpdir_manager(base_dir='/tmp') as query_tmp_dir:
            input_path = os.path.join(query_tmp_dir, 'query.a3m')
            hhr_path = os.path.join(query_tmp_dir, 'output.hhr')
            with open(input_path, 'w') as f:
                f.write(a3m)

            db_cmd = []
            for db_path in self.databases:
                db_cmd.append('-d')
                db_cmd.append(db_path)
            cmd = [self.binary_path,
                   '-i', input_path,
                   '-o', hhr_path,
                   '-maxseq', str(self.maxseq),
                   '-cpu', '8',] + db_cmd

            logging.info('Launching subprocess "%s"', ' '.join(cmd))
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            with timing('HHsearch query'):
                stdout, stderr = process.communicate()
                retcode = process.wait()
            if retcode:
                # Stderr is truncated to prevent proto size errors in Beam.
                raise RuntimeError('HHSearch failed:\nstdout:\n%s\n\nstderr:\n%s\n' % (
                    stdout.decode('utf-8'), stderr[:100_000].decode('utf-8')))
            with open(hhr_path) as f:
                hhr = f.read()
        return hhr


class Jackhmmer:
    """Python wrapper of the Jackhmmer binary."""

    def __init__(self,
                 *,
                 binary_path: str,
                 database_path: str,
                 n_cpu: int = 8,
                 n_iter: int = 1,
                 e_value: float = 0.0001,
                 z_value: Optional[int] = None,
                 get_tblout: bool = False,
                 filter_f1: float = 0.0005,
                 filter_f2: float = 0.00005,
                 filter_f3: float = 0.0000005,
                 incdom_e: Optional[float] = None,
                 dom_e: Optional[float] = None):
        """Initializes the Python Jackhmmer wrapper.

        Args:
          binary_path: The path to the jackhmmer executable.
          database_path: The path to the jackhmmer database (FASTA format).
          n_cpu: The number of CPUs to give Jackhmmer.
          n_iter: The number of Jackhmmer iterations.
          e_value: The E-value, see Jackhmmer docs for more details.
          z_value: The Z-value, see Jackhmmer docs for more details.
          get_tblout: Whether to save tblout string.
          filter_f1: MSV and biased composition pre-filter, set to >1.0 to turn off.
          filter_f2: Viterbi pre-filter, set to >1.0 to turn off.
          filter_f3: Forward pre-filter, set to >1.0 to turn off.
          incdom_e: Domain e-value criteria for inclusion of domains in MSA/next
            round.
          dom_e: Domain e-value criteria for inclusion in tblout.
        """
        self.binary_path = binary_path
        self.database_path = database_path

        if not os.path.exists(self.database_path):
            logging.error(
                'Could not find Jackhmmer database %s',
                database_path)
            raise ValueError(
                f'Could not find Jackhmmer database {database_path}')

        self.n_cpu = n_cpu
        self.n_iter = n_iter
        self.e_value = e_value
        self.z_value = z_value
        self.filter_f1 = filter_f1
        self.filter_f2 = filter_f2
        self.filter_f3 = filter_f3
        self.incdom_e = incdom_e
        self.dom_e = dom_e
        self.get_tblout = get_tblout

    def query(self, input_fasta_path: str) -> Mapping[str, Any]:
        """Queries the database using Jackhmmer."""
        with tmpdir_manager(base_dir='/tmp') as query_tmp_dir:
            sto_path = os.path.join(query_tmp_dir, 'output.sto')

            # The F1/F2/F3 are the expected proportion to pass each of the filtering
            # stages (which get progressively more expensive), reducing these
            # speeds up the pipeline at the expensive of sensitivity.  They are
            # currently set very low to make querying Mgnify run in a reasonable
            # amount of time.
            cmd_flags = [
                # Don't pollute stdout with Jackhmmer output.
                '-o', '/dev/null',
                '-A', sto_path,
                '--noali',
                '--F1', str(self.filter_f1),
                '--F2', str(self.filter_f2),
                '--F3', str(self.filter_f3),
                '--incE', str(self.e_value),
                # Report only sequences with E-values <= x in per-sequence
                # output.
                '-E', str(self.e_value),
                '--cpu', str(self.n_cpu),
                '-N', str(self.n_iter)
            ]
            if self.get_tblout:
                tblout_path = os.path.join(query_tmp_dir, 'tblout.txt')
                cmd_flags.extend(['--tblout', tblout_path])

            if self.z_value:
                cmd_flags.extend(['-Z', str(self.z_value)])

            if self.dom_e is not None:
                cmd_flags.extend(['--domE', str(self.dom_e)])

            if self.incdom_e is not None:
                cmd_flags.extend(['--incdomE', str(self.incdom_e)])

            cmd = [self.binary_path] + cmd_flags + [input_fasta_path, self.database_path]

            logging.info('Launching subprocess "%s"', ' '.join(cmd))
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            with timing(f'Jackhmmer ({os.path.basename(self.database_path)}) query'):
                _, stderr = process.communicate()
                retcode = process.wait()

            if retcode:
                raise RuntimeError('Jackhmmer failed\nstderr:\n%s\n' % stderr.decode('utf-8'))

            # Get e-values for each target name
            tbl = ''
            if self.get_tblout:
                with open(tblout_path) as f:
                    tbl = f.read()

            with open(sto_path) as f:
                sto = f.read()

        raw_output = dict(sto=sto, tbl=tbl, stderr=stderr, n_iter=self.n_iter, e_value=self.e_value)
        return raw_output
