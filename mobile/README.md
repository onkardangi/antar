# Antar Mobile

React Native / Expo client for Antar.

## Current status

The mobile application currently includes:

- Foundation connectivity screen
- Library screen (canonical Chapter list)
- Chapter detail with Verse list
- Verse Reader (Sanskrit)
- Local-only Reading Progress foundation (persists last-read Verse; no Home / Continue Reading UI yet)

No Home, Reflection, Journey, Search, Guidance, Understanding, Saar, transliteration, commentary, authentication, cloud sync, or bottom navigation yet.

## Stack

- React Native
- TypeScript
- Expo SDK 57
- React Navigation native stack
- Lora and Source Sans 3 via `@expo-google-fonts/*` and `expo-font`

## Setup

Requires Node.js `>=22.13.0` (CI uses `22.13.1`).

```bash
cd mobile
npm ci
```

Optional local environment file:

```bash
cp .env.example .env
```

## Fonts

Library handoff typography loads at bootstrap through `AppFonts`:

- `Lora_400Regular`
- `Lora_400Regular_Italic`
- `SourceSans3_400Regular`

Fonts are installed with:

```bash
npm install expo-font @expo-google-fonts/lora @expo-google-fonts/source-sans-3
```

Until fonts finish loading, the app shows an empty background fill rather than rendering with permanent substitute typefaces.

## Start

```bash
npm start
```

Platform launch helpers:

```bash
npm run ios
npm run android
```

iOS and Android are the supported targets. Web is not part of Antar V1.

## API base URL configuration

Set `EXPO_PUBLIC_API_BASE_URL` before starting Expo.

| Runtime | Typical value |
| --- | --- |
| iOS simulator | `http://localhost:8080` |
| Android emulator | `http://10.0.2.2:8080` |
| Physical device | `http://<your-lan-ip>:8080` |

If unset, development defaults are:

- Android emulator → `http://10.0.2.2:8080`
- other platforms → `http://localhost:8080`

Physical devices must override the value. `localhost` on a phone points at the phone, not your development machine.

## Navigation decision

The product shell uses React Navigation (`@react-navigation/native` + native stack):

```text
Library (initial)
ChapterPlaceholder
FoundationStatus (local validation)
```

See `src/navigation/NAVIGATION.md`.

Note: Expo CLI may mention `src/app` in relation to Expo Router because that directory name overlaps Expo Router conventions. This project does **not** use Expo Router. Entry remains `index.ts` → `App.tsx`, and navigation lives under `src/navigation/`.

## Storage boundaries

- **Secure storage** — `expo-secure-store` backs `ExpoSecureStoreAdapter` for future authentication secrets. No tokens are stored and no authentication flow exists yet.
- **Ordinary local storage** — `@react-native-async-storage/async-storage` backs `AsyncStorageAdapter` for non-secret state such as Reading Progress (`antar.reading-progress.v1`).

## Commands

```bash
npm run typecheck
npm run lint
npm test
npm run expo:config
```

## Source layout

```text
src/
├── app/
├── navigation/
├── features/
├── design-system/
├── services/
├── shared/
├── storage/
└── test/
```
