# Antar Mobile

React Native / Expo client for Antar.

## Current status

The mobile application currently contains only the foundation connectivity screen.
No product features, product screens, authentication flows, or business navigation routes have been implemented.

## Stack

- React Native
- TypeScript
- Expo SDK 57
- React Navigation native stack

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

The foundation shell uses React Navigation (`@react-navigation/native` + native stack) with one screen:

```text
FoundationStatusScreen
```

See `src/navigation/NAVIGATION.md`.

Note: Expo CLI may mention `src/app` in relation to Expo Router because that directory name overlaps Expo Router conventions. This project does **not** use Expo Router. Entry remains `index.ts` → `App.tsx`, and navigation lives under `src/navigation/`.

## Secure storage boundary

`expo-secure-store` backs `ExpoSecureStoreAdapter` so future authentication can store secrets outside AsyncStorage.
No tokens are stored and no authentication flow exists yet.

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
