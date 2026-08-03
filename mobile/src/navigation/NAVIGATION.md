# Mobile Navigation Decision

## Choice

React Navigation with a native stack:

- `@react-navigation/native`
- `@react-navigation/native-stack`

## Why

- Fits the approved `src/navigation/` layout without Expo Router's root `app/` convention.
- Maintained and widely used with Expo.
- Keeps the foundation shell to a single explicit screen.
- Leaves Expo Router as an open option for later product navigation.

## Current shell

```text
RootNavigator
└── FoundationStatus
```

No bottom tabs, authentication flow, or product routes yet.
