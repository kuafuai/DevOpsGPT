const GOOGLE_ORIGIN = 'https://github.com';


siderPanelPath = "sidepanel.html"


chrome.tabs.onActivated.addListener(async ({tabId}) => {
    // console.log("活跃的页面id", tabId)
    // messageTabid = tabId
    // console.log("切换页面活跃的是",activeInfo)
    try {
        let tab = await chrome.tabs.get(tabId);
        if (tab === undefined) {
            return;
        }
        let tabs = await chrome.tabs.query({windowId: tab.windowId});
        for (let i = 0; i < tabs.length; i++) {
            // console.log(tabs[i])
            // if (tabs[i].id !== tabId) {
            //     console.log("active 不是当前页面", tabs[i].id)
            // chrome.sidePanel.setOptions({
            //     tabId: tabs[i].id,
            //     enabled: false
            // })
            // } else {
            //     console.log("active 是当前页面", tabs[i].id)
            //     chrome.sidePanel.setOptions({
            //         tabId: tabs[i].id,
            //         enabled: true
            //     })
            // }
        }
        // if (tabId !== undefined) {
        //     let tab = await chrome.tabs.get(tabId);
        //     console.log("活跃的页面是", tab)
        //     let url = new URL(tab.url);
        //     // 如果切换的是github页面
        //     if (url.origin === GOOGLE_ORIGIN) {
        //         await chrome.sidePanel.setOptions({
        //             tabId,
        //             path: "sidepanel.html",
        //             // enabled: true
        //         });
        //     } else {
        //         await chrome.sidePanel.setOptions({
        //             tabId,
        //             // path: "sidepanel.html",
        //             enabled: false
        //         });
        //     }
        // }
        // console.log(tab)
    } catch (e) {
        console.log(Date.now(), e)
    }

});

chrome.tabs.onUpdated.addListener(async (tabId, info, tab) => {

    // console.log("update......")
    if (info.status === 'complete' && tab.url.includes('github.com')) {
        // if (info.url){
        // console.log("complete ", tabId)
        // chrome.scripting
        chrome.scripting.executeScript({
            target: {tabId: tabId},
            files: ['content-script.js']
        });
    }

    if (!tab.url) return;
    const url = new URL(tab.url);
    siderPanelPath = "sidepanel.html"
    if (url.origin === GOOGLE_ORIGIN) {
        // console.log("在github页面")
        await chrome.sidePanel.setOptions({
            tabId,
            path: "sidepanel.html",
            // enabled: true
        });
    } else {
        // console.log("不在github页面")
        await chrome.sidePanel.setOptions({
            tabId,
            path: "sidepanel.html",
            enabled: false
        });
    }

    // let tabs = await chrome.tabs.query({windowId: tab.windowId});
    // for (let i = 0; i < tabs.length; i++) {
    //     // console.log(tabs[i])
    //     if (tabs[i].id !== tabId) {
    //         console.log("onUpdated 不是当前页面", tabs[i].id)
    //         chrome.sidePanel.setOptions({
    //             tabId: tabs[i].id,
    //             enabled: false
    //         })
    //     } else {
    //         console.log("onUpdated 是当前页面", tabs[i].id)
    //         chrome.sidePanel.setOptions({
    //             tabId: tabs[i].id,
    //             enabled: true
    //         })
    //     }
    // }
});

let id = ""
let lockset = undefined;
// 接收消息
chrome.runtime.onMessage.addListener(async (message, sender) => {
    // siderPanelPath = "mainsidepanel.html"
    // (async () => {

    if (message.type === 'open_side_panel') {
        console.log(Date.now(), "service-worker  from content-js, type is  open_side_panel", message)
        siderPanelPath = "sidepanel.html"
        let url = ""

        // await chrome.sidePanel.setOptions({
        //     tabId: sender.tab.id,
        //     path: 'sidepanel.html',
        //     enabled: true
        // });

        chrome.sidePanel.open({tabId: sender.tab.id});


        const min = 500;
        const max = 1000;
        const randomTime = Math.floor(Math.random() * (max - min + 1)) + min;
        console.log(Date.now(), "random time", randomTime);

        setTimeout(() => {
            try {
                if (lockset === undefined) {
                    lockset = 0;
                    let respose = {type: 'action_analyzer', data: message.data, tabid: sender.tab.id};
                    console.log(Date.now(), "service-worker to sidepanel, type is  action_analyzer", respose)
                    chrome.runtime.sendMessage(respose);
                }
            } catch (e) {
                console.log(e)
            }

        }, randomTime)

        // 1100毫秒之后取消锁
        setTimeout(() => {
            lockset = undefined
        }, 1300)
        // setTimeout(async ()=>{·
        // await chrome.sidePanel.open({tabId: sender.tab.id});
        // },100)

        // await chrome.sidePanel.setOptions({
        //     tabId: sender.tab.id,
        //     path: 'sidepanel.html',
        //     enabled: true
        // });


        // url = tab.url
        // id = tab.id
        // console.log("接收消息的侧边栏", sender.tab.id)


    } else if (message.type === "get_current_tabid") {
        console.log(Date.now(), "service-worker from content-js ,type is  get_current_tabid", message)
        let tabs = await chrome.tabs.query({windowId: sender.tab.windowId});
        for (let i = 0; i < tabs.length; i++) {
            let taburl = tabs[i].url;
            if (taburl) {
                // 如果是github页面，只放行当前活跃的页面
                let taburlTemp = new URL(taburl);
                if (taburlTemp.origin === GOOGLE_ORIGIN) {
                    if (tabs[i].id !== sender.tab.id) {
                        // console.log("不是当前页面", tabs[i].id)
                        // chrome.sidePanel.getOptions({tabId: tabs[i].id}, options => {
                        //
                        //     console.log("实例是",options.)
                        //     if (options == null) {
                        //         chrome.sidePanel.setOptions({
                        //             tabId: tabs[i].id,
                        //             path: "sidepanel.html",
                        //             enabled: false
                        //         })
                        //     } else {
                        //         options.enabled = false;
                        //     }
                        // })
                        chrome.sidePanel.setOptions({
                            tabId: tabs[i].id,
                            path: "sidepanel.html",
                            enabled: false
                        })
                    } else {
                        // console.log("是当前页面", tabs[i].id)
                        chrome.sidePanel.setOptions({
                            tabId: tabs[i].id,
                            path: "sidepanel.html",
                            enabled: true
                        })
                    }
                } else {
                    // 如果不是github所属页面，直接取消侧边栏
                    chrome.sidePanel.setOptions({
                        tabId: tabs[i].id,
                        path: "sidepanel.html",
                        enabled: false
                    })
                }
            }
            // console.log(tabs[i])

        }
        console.log(Date.now(), "service-work to content-js ,type is get_current_tabid ")
        chrome.tabs.sendMessage(sender.tab.id, {type: "get_current_tabid", data: message.data, tabid: sender.tab.id})
    } else if (message.type === "prepare_send_message") {
        console.log("service-work from sidepanel ,type is prepare_send_message", message)
    }
});

