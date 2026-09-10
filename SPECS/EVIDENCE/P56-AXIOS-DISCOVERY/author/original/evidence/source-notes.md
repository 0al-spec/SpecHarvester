# Portable Source Provenance

Repository: https://github.com/axios/axios
Pinned revision: 509719387e4993392ca40da03a49678269cdfb90

The excerpts in this package were copied unchanged from the pinned snapshot.
The listed digests are SHA-256 digests of the complete source files, not of the
excerpts.

| Package evidence | Source path | Source range | Full-file SHA-256 |
| --- | --- | --- | --- |
| `evidence/README-excerpt.md` | `README.md` | lines 444-458, 548-590, 670-760, 1198-1248, 1474-1608 | `4db033f8e5c39cc3427078df94ebe079a37a7c6e557180e6f616638af5e3358f` |
| `evidence/index-types-excerpt.md` | `index.d.ts` | lines 380-480, 642-775 | `3768eb0975f030352ec96190aaa485af41910029d9a62d9c70557c976b30a6f7` |
| `evidence/LICENSE` | `LICENSE` | lines 1-14 | `82761059eaedacb3356803aea8a170d8298609f91b14fc32ee1bfb40d690183c` |
| `evidence/package-metadata.md` | `package.json` | lines 1-18, 31-45, 55-72, 93-103 | `c9afce8c65c9fadaebaac41ca90db26779efdc5e95aeca49b4e9477b61bcc4b2` |

Open questions for review: this candidate does not independently establish
which adapter is selected in every supported runtime, the complete response
type matrix, or the behavior of all configuration fields. The source snapshot
also contains version-sensitive documentation examples; this package keeps the
boundary at the pinned package version and does not claim universal support.
