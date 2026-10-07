# Public no-LaTeX audit compatibility

The first public-clone endpoint audit stopped before numerical verification:
its immutable original manifest listed `source_snapshot/endpoint_calibration_derivation.tex`,
intentionally absent under the user's no-LaTeX publication rule. No numerical
file was missing and no research result changed.

The live checker now has an explicit `--allow-excluded-latex` option. Only
missing `.tex` files within `source_snapshot` may be omitted. Every omission
is printed with its original hash and the statement that it was not verified.
The report sets `complete_original_manifest_verified` to false. Remaining
hashes and every numerical ledger undergo the original independent checks;
any missing non-TeX file still raises an error. The default strict audit remains.

Tests ran on the actual no-LaTeX staging clone, without overwriting original
evidence or rerunning a scientific experiment. Endpoint:17 available hashes,
8 ledgers,666 nodes, maximum discrepancy5.366e-64. Importance:44 available
hashes,32 ledgers,2684 nodes, maximum discrepancy1.4173e-63. Each reported
one omitted proof-source hash, not a verified original full manifest.
Reports are in `public_snapshot_audit_v1/`.

The mathematical proofs remain available in the sole uploaded derivation PDF.
Local TeX proof snapshots and original audit reports are unchanged. This is
packaging compatibility, not a new mathematical result or experiment.
