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
├── Home (initial)
├── Library
├── Chapter
├── VerseReader
└── FoundationStatus (local validation)
```

Native stack chrome is hidden; product screens use the shared `ScreenHeader`
from the design system.

## Primary flows

```text
Home
  ├── Today's Invitation → VerseReader
  └── Browse Bhagavad Gita → Library → Chapter → VerseReader
```

Back follows normal stack history:

- Library Back → Home (when Library was opened from Home)
- Chapter Back → Library
- VerseReader Back → previous screen (Home or Chapter)

Back is passed only when `navigation.canGoBack()` is true. Home is the root
route, so ScreenHeader omits Back there.

No bottom tabs, Settings entry, or authentication flow yet.

## Chapter params

```text
chapterId
chapterNumber
```

## VerseReader params

```text
verseId
verseNumber
chapterNumber
```
