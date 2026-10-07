# Initial metadata-reader failure

The first bounded inspection stopped with a UTF-8 decoding error before its report was written. The archive includes macOS AppleDouble files named `._pairs.csv`, `._top16_images.csv` and `._activations.csv`; these are binary filesystem metadata, not the actual CSV tables. A header-only diagnostic identified this cause. No feature fitting, pair selection or risk computation occurred.

The corrected reader explicitly ignores those metadata members, preserves their names and sizes in its report, and reads only the activation CSV's column header (not its activation values). The resource eligibility requirements, data budget and stopping criteria are unchanged. This is a parsing correction, not a scientific protocol change.
