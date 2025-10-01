// --- Tolgee i18n initialization and language switcher ---

// 1. Detect language from URL or localStorage, default to 'de-DE'
const url = new URL(window.location.href);
const currentLang = url.searchParams.get('lang') || localStorage.getItem('preferredLang') || 'de-DE';
localStorage.setItem('preferredLang', currentLang);

// 2. Preselect language in dropdown and set up change handler
document.addEventListener('DOMContentLoaded', () => {
  const selector = document.getElementById('demo-category');
  if (selector) {
    selector.value = currentLang;
    selector.addEventListener('change', function () {
      localStorage.setItem('preferredLang', this.value);
      url.searchParams.set('lang', this.value);
      window.location.href = url.toString(); // Reload with new lang param
    });
  }
});

// 3. Initialize Tolgee with config from backend
const { Tolgee, InContextTools, FormatSimple, BackendFetch } = window['@tolgee/web'];
const tolgee = Tolgee()
  .use(InContextTools())
  .use(FormatSimple())
  .use(BackendFetch())
  .init({
    apiKey: window.tolgeeConfig.apiKey,
    apiUrl: window.tolgeeConfig.apiUrl,
    language: currentLang,
    observerType: 'text',
    observerOptions: { inputPrefix: '{{', inputSuffix: '}}' },
  });

// 4. Run Tolgee and translate elements with [data-i18n]
tolgee.run().then(() => {
  const t = tolgee.t;
  document.querySelectorAll('[data-i18n]').forEach((el) => {
    const key = el.getAttribute('data-i18n');
    const attr = el.getAttribute('data-i18n-attr');
    if (attr) {
      el.setAttribute(attr, t(key));
    } else {
      el.innerHTML = t(key);
    }
  });
});