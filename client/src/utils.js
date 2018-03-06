// matchMedia polyfill for
// https://github.com/WickyNilliams/enquire.js/issues/82
let enquire;
if (typeof window !== 'undefined') {
    const matchMediaPolyfill = (mediaQuery: string): MediaQueryList => {
        return {
            media: mediaQuery,
            matches: false,
            addListener() {
            },
            removeListener() {
            },
        };
    };
    window.matchMedia = window.matchMedia || matchMediaPolyfill;
    enquire = require('enquire.js'); // eslint-disable-line global-require
}

export function getMenuItems(moduleData, locale) {
    const menuMeta = moduleData.map(item => item.meta);
    const menuItems = {};
    menuMeta.sort(
        (a, b) => (a.order || 0) - (b.order || 0)
    ).forEach((meta) => {
        const category = (meta.category && meta.category[locale]) || meta.category || 'topLevel';
        if (!menuItems[category]) {
            menuItems[category] = {};
        }

        const type = meta.type || 'topLevel';
        if (!menuItems[category][type]) {
            menuItems[category][type] = [];
        }

        menuItems[category][type].push(meta);
    });
    return menuItems;
}

export function isZhCN(pathname) {
    return /-cn\/?$/.test(pathname);
}

export function getLocalizedPathname(path, zhCN) {
    const pathname = path.startsWith('/') ? path : `/${path}`;
    if (!zhCN) { // to enUS
        return /\/?index-cn/.test(pathname) ? '/' : pathname.replace('-cn', '');
    } else if (pathname === '/') {
        return '/index-cn';
    } else if (pathname.endsWith('/')) {
        return pathname.replace(/\/$/, '-cn/');
    }
    return `${pathname}-cn`;
}

export function ping(callback) {
    // eslint-disable-next-line
    const url = 'https://private-a' + 'lipay' + 'objects.alip' + 'ay.com/alip' + 'ay-rmsdeploy-image/rmsportal/RKuAiriJqrUhyqW.png';
    const img = new Image();
    let done;
    const finish = (status) => {
        if (!done) {
            done = true;
            img.src = '';
            callback(status);
        }
    };
    img.onload = () => finish('responded');
    img.onerror = () => finish('error');
    img.src = url;
    return setTimeout(() => finish('timeout'), 1500);
}

export function isLocalStorageNameSupported() {
    const testKey = 'test';
    const storage = window.localStorage;
    try {
        storage.setItem(testKey, '1');
        storage.removeItem(testKey);
        return true;
    } catch (error) {
        return false;
    }
}

export function enquireScreen(cb) {
    if (!enquire) {
        return;
    }
    /* eslint-disable no-unused-expressions */
    // and (min-width: 320px)
    enquire.register('only screen and (max-width: 768px)', {
        match: () => {
            cb && cb(true);
        },
        unmatch: () => {
            cb && cb();
        },
    });
    /* eslint-enable no-unused-expressions */
}