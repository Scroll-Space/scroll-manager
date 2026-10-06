import { PluginStorage } from './scroll-core/m_storage.js';
import { EditorController } from './scroll-core/m_editor.js';

const plugStore = new PluginStorage(window);
const editorCtrl = new EditorController(window);
let panelWindow = null;

window.Asc.plugin.init = function () {
    // Добавляем на вкладку плагинов кнопку для открытия панели
    setupToolbar();

    // Если в текущей сессии не востанавливался скролл, то пытаемся его восстановить
    if (!plugStore.getIsRestoredFlag()) {
        tryRestoreScroll();
        // Указываем что сколл был восстановлен,
        // чтобы не восстанавливать его повторно в этой сессии
        plugStore.setIsRestoredFlag(true);
    }

    // Таймер для сохранения текущего скролла в локальное хранилище
    startTempScrollSaver();    
};

function setupToolbar() {
    // Добавляем на вкладку плагинов кнопку для открытия панели
    window.Asc.plugin.executeMethod("AddToolbarMenuItem", [{
        guid: window.Asc.plugin.guid,
        tabs: [
            {
                id: "plugins",
                text: "Scroll Manager",
                items: [
                    {
                        id: "openScrollPanelBtn",
                        type: "button",
                        text: "Scroll Manager",
                        hint: "Open scroll panel",
                        split: false,
                        enableToggle: false,
                        lockInViewMode: false,
                        icons: "resources/icons/icon%state%(normal)%scale%(default|*).%extension%(svg|png)"
                    },
                ],
            },
        ],
    }]);

    // Обработчик клика по кнопке открытияпанели
    window.Asc.plugin.attachToolbarMenuClickEvent("openScrollPanelBtn", function () {
        if (!panelWindow) {
            panelWindow = new window.Asc.PluginWindow();
        }

        panelWindow.show({
            url: "panel.html",
            description: "Scroll Manager",
            type: "panel",
            isVisual: true,
            isViewer: true,
            EditorsSupport: ["pdf"],
            guid: window.Asc.plugin.guid
        });
        panelWindow.activate(true);
    });
}

function tryRestoreScroll() {
    if (!plugStore.getSaveByCloseFlag()) return;

    let savedView = plugStore.getView();
    let tempSavedView = plugStore.getView(true);

    // При загрузке плагина, если есть временный скролл, то он становится основным
    if (tempSavedView !== null && isViewDifferent(savedView, tempSavedView) && plugStore.getSaveByCloseFlag()) {
        savedView = tempSavedView;
        plugStore.saveView(savedView);
    }

    if (savedView === null) return;

    editorCtrl.setView(savedView);

}

// Минималистичный таймер, который почти не тратит CPU
function startTempScrollSaver() {
    setInterval(() => {
        if (!plugStore.getSaveByCloseFlag()) return;

        const currentView = editorCtrl.getView();

        if (currentView === null) return;

        let tempSavedView = plugStore.getView(true);

        if (tempSavedView === null || isViewDifferent(currentView, tempSavedView)) {
            plugStore.saveView(currentView, true);
        }
    }, 1000);
}

function isViewDifferent(view1, view2) {
    // Если один из них null, а другой нет — они не равны
    if (!view1 || !view2) return view1 !== view2;

    // Сравниваем поля напрямую
    return view1.x !== view2.x ||
        view1.y !== view2.y ||
        view1.zoom !== view2.zoom;
}

window.Asc.plugin.button = function (id) {
    // ONLYOFFICE передает id = -1 при нажатии на крестик боковой панели
    if (Number(id) === -1) {
        panelWindow?.close();
        panelWindow = null;
    }
};
