# Tested installation

This page identifies the installation that opened successfully. It contains only installation details.

| Component | Working installation |
| --- | --- |
| Linux desktop | Zorin OS 18.1, Ubuntu Noble base |
| Wine | 10.0; package `10.0~repack-6ubuntu1+zorin5` |
| Prefix architecture | `win32` |
| Blue Iris | 5.9.9.98, 32-bit |
| Bootstrap installer | Blue Iris 4.8.6.3 |
| App-local dependencies copied from BI 4 | `SeaMAX.dll`, `ftd2xx.dll`, `msvcr120.dll`, `msvcp120.dll` |
| Custom Wine DLL overrides | None in the working installation |

The BI 5 update was extracted with 7-Zip into `C:\Program Files\Blue Iris 5`. The four dependencies were copied beside its executable, which then opened using system Wine 10.

## Historical vendor packages

These official URLs identify the packages used at the time. Availability and the contents of rolling download links can change. The hashes identify the actual files used; they do not guarantee that today's download is the same file.

| Package | Historical official URL | SHA-256 |
| --- | --- | --- |
| BI 4.8.6.3 installer | `https://blueirissoftware.com/BlueIris_48603.exe` | `5dad7d0d9c2634f44ccc37004f6cd6009f085e73fd2324fedbb62089b763460a` |
| BI 5 32-bit update | `https://blueirissoftware.com/50/update32.exe` | `70f1f8740421854906749b55bc890eca76411f9516e6475da13bc28bb4c7abc5` |

No vendor files are redistributed here. The generalized installation instructions and helper scripts have not been tested as a complete fresh installation. Other distributions, Wine builds and BI versions may behave differently.
