# Web Chat UI – Language Toggle: Design Proposal

This document proposes an optional front-end feature to add a **language toggle** to the GitHub Copilot web Chat UI, allowing users to switch the interface to Simplified Chinese (or other languages) without leaving the page.

---

## Motivation

Currently the web Chat UI language follows either:
1. The GitHub account display language, or
2. The browser's preferred language setting.

Neither option is discoverable from within the Chat UI itself. A lightweight in-page toggle would let users change the language instantly and remember their choice across sessions.

---

## Proposed Feature: Language Toggle Button

### UI Placement

Add a small 🌐 icon button (or a text label like **EN | 中文**) in the top-right corner of the Chat header bar, next to the existing settings/account icons.

```
┌────────────────────────────────────────────────┐
│  ◉ Copilot Chat          🌐 EN | 中文   ⚙  👤  │
├────────────────────────────────────────────────┤
│                                                │
│         (conversation area)                    │
│                                                │
└────────────────────────────────────────────────┘
```

Clicking the toggle cycles between available locales (e.g., `en-US` → `zh-CN` → `en-US`).

---

## Storing the User Preference

### Option A – User Settings API (recommended for authenticated users)

Persist the preference server-side via GitHub's user settings API so it roams across devices.

```pseudo
// Write preference
PUT /api/user/settings
{
  "chat_ui_language": "zh-CN"
}

// Read preference on page load
GET /api/user/settings
→ { "chat_ui_language": "zh-CN" }
```

### Option B – localStorage (lightweight fallback)

Store the preference in the browser for unauthenticated or guest sessions.

```javascript
// Write preference
localStorage.setItem('chatUiLanguage', 'zh-CN');

// Read preference
const lang = localStorage.getItem('chatUiLanguage') || navigator.language || 'en-US';
```

### Resolution order (suggested)

```
User Settings API value
  ↓ (fallback if not set)
localStorage value
  ↓ (fallback if not set)
GitHub account display language (from session)
  ↓ (fallback if not available)
Browser navigator.language
  ↓ (final fallback)
'en-US'
```

---

## Applying i18n Resource Selection

The UI should load locale strings based on the resolved language, with `zh-CN` falling back to the user's GitHub account language and ultimately to English.

```javascript
/**
 * Resolve the display language for the Chat UI.
 * Falls back through: user pref → account lang → browser lang → 'en-US'
 */
function resolveLanguage(userPref, accountLang) {
  const supported = ['en-US', 'zh-CN', 'ja-JP', 'es-ES']; // extend as needed
  const candidates = [
    userPref,           // explicit user choice
    accountLang,        // GitHub account language
    navigator.language, // browser language
    'en-US',            // final fallback
  ];
  for (const lang of candidates) {
    if (!lang) continue;
    if (supported.includes(lang)) return lang;
    // Try matching just the base language tag (e.g. 'zh' matches 'zh-CN')
    const baseTag = lang.split('-')[0];
    if (baseTag) {
      const base = supported.find(s => s.startsWith(baseTag + '-') || s === baseTag);
      if (base) return base;
    }
  }
  return 'en-US';
}

/**
 * Load and apply i18n resources for the resolved language.
 */
async function applyLocale(lang) {
  if (!supported.includes(lang)) lang = 'en-US'; // guard against unexpected values
  const messages = await import(`./locales/${lang}.json`);
  i18n.setMessages(messages.default); // replace with actual i18n library call
  document.documentElement.lang = lang;
}

// On page load
const userPref  = localStorage.getItem('chatUiLanguage')
                  || await fetchUserSettingLanguage(); // User Settings API
const accountLang = window.__GITHUB_SESSION__?.displayLanguage; // injected server-side
const resolved  = resolveLanguage(userPref, accountLang);
await applyLocale(resolved);
```

### Locale file structure (example)

```
src/
  locales/
    en-US.json   ← default
    zh-CN.json   ← Simplified Chinese
    ja-JP.json
```

**`zh-CN.json` excerpt:**

```json
{
  "chat.placeholder": "向 Copilot 提问…",
  "chat.newConversation": "新建对话",
  "chat.suggestions": "建议",
  "settings.language": "语言",
  "settings.languageToggle": "切换语言"
}
```

---

## Toggle Component (pseudo-code / React-like)

```jsx
function LanguageToggle({ currentLang, onChange }) {
  const options = [
    { value: 'en-US', label: 'EN' },
    { value: 'zh-CN', label: '中文' },
  ];

  return (
    <div className="language-toggle" aria-label="Select language">
      {options.map(opt => (
        <button
          key={opt.value}
          className={currentLang === opt.value ? 'active' : ''}
          onClick={() => onChange(opt.value)}
          aria-pressed={currentLang === opt.value}
        >
          {opt.label}
        </button>
      ))}
    </div>
  );
}

// On change handler
function handleLanguageChange(newLang) {
  localStorage.setItem('chatUiLanguage', newLang);
  // Optionally persist to User Settings API:
  // await saveUserSetting('chat_ui_language', newLang);
  applyLocale(newLang);
}
```

---

## Summary

| Aspect | Recommendation |
|---|---|
| Preference storage | User Settings API (auth) + localStorage fallback |
| Fallback chain | User pref → account lang → browser lang → `en-US` |
| Default for zh-CN users | `zh-CN` if GitHub account language is `zh-CN` |
| UI placement | Header bar, top-right |
| Supported locales (initial) | `en-US`, `zh-CN` |

---

## Related

- [set-chat-language-zh.md](./set-chat-language-zh.md) – End-user guide (Chinese) for switching Chat UI to Simplified Chinese
