# Mobile Navigation Decision

## Choice

React Navigation with a native stack:

- `@react-navigation/native`
- `@react-navigation/native-stack`

## Why

- Fits the approved `src/navigation/` layout without Expo Router's root `app/` convention.
- Maintained and widely used with Expo.
- Leaves Expo Router as an open option for later product navigation.

## Current routes

```text
RootNavigator
├── Library (initial)
├── ChapterPlaceholder
└── FoundationStatus (local validation)
```

Native stack chrome is hidden; Library and ChapterPlaceholder use the shared
`ScreenHeader` from the design system.

Back is passed only when `navigation.canGoBack()` is true. While Library is the
root route, ScreenHeader shows the application title without a Back action.

No bottom tabs, Settings entry, or authentication flow yet. Verse lists are deferred.

## ChapterPlaceholder params

```text
chapterId
chapterNumber
```

`chapterId` is retained because the existing navigation contract already used it.
Handoff requires `chapterNumber`; additional display fields are not passed.
