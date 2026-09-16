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

### Build
GitHub Actions builds a Linux x86_64 AppImage.

### RetroAchievements API key
The application will ask each user for their own RetroAchievements API key. It is stored locally and is never embedded in the source tree or release binary.

## License
MIT
