# RD-CM
## RetroDECK Collection Manager

A Linux desktop application for managing RetroDECK / ES-DE collections.

### Planned features
- RetroAchievements ROM identification using RAHasher
- Report of ROMs whose RA hashes are not found
- ES-DE gamelist management
- Custom RetroAchievements and Couch Coop collections
- Automatic RetroDECK directory detection
- Backups before modifying collections

### Build & Download

GitHub Actions builds the Linux x86_64 AppImage automatically.

The latest ready-to-use AppImage is available under
**[Releases](https://github.com/dema182/RD-CM/releases)**.

Development builds are also available as GitHub Actions artifacts.

### Installation

No installation is required.

1. Download the latest `RD-CM-x86_64.AppImage` from the Releases page.
2. Make the file executable:
   ```bash
   chmod +x RD-CM-x86_64.AppImage

### RetroAchievements API key
The application will ask each user for their own RetroAchievements API key. It is stored locally and is never embedded in the source tree or release binary.

## License
MIT
