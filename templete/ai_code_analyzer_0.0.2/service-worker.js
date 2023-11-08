const GOOGLE_ORIGIN = 'https://github.com';


// chrome.sidePanel
//     .setPanelBehavior({openPanelOnActionClick: true})
//     .catch((error) => console.error(error));
// function clickElement(elementSelector) {
//     let htmlBodyElement = document.querySelector("body");
//     let htmlButtonElement = document.createElement("button");
//     htmlButtonElement.innerText = "backgroud"
//     htmlBodyElement.appendChild(htmlButtonElement)
//     console.log("触发background加载函数")
// }


/**
 * 更新页面
 */

// chrome.browserAction.onClicked.addListener(function(tab) {
//     // chrome.tabs.executeScript(tab.id, {file: 'jquery.min.js'});
//     chrome.tabs.executeScript(tab.id, {file: 'content-script.js'});
// });

siderPanelPath = "sidepanel.html"

// chrome.webNavigation.onHistoryStateUpdated.addListener(function (details) {
//     console.log("service ", details.tabId)
//     // chrome.scripting.executeScript({
//     //     target: {tabId: details.tabId},
//     //     files: ['content-script.js'],
//     //
//     // });
//     // chrome.scripting.executeScript({
//     //     target: {tabId: details.tabId},
//     //     files: ['content-script.js']
//     // });
//     console.log("页面加载完成，注入content-script",details.tabId,details.url)
//
// });

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
    // console.log(info.url, "更新",tabId)
    // chrome.scripting.executeScript({
    //     target: {tabId: tabId},
    //     files: ['content-script.js'],
    //
    // });
    // let [tab] = await chrome.tabs.query({active: true, currentWindow: true})
    // url = tab.url
    // id = tab.id
    // chrome.tabs.sendMessage(tabId, {type: "test", data: "测试"})
//         console.log(info.url, "更新")
//         let script = document.createElement('script');
// // 设置脚本的 URL
//         script.src = chrome.runtime.getURL('content-script.js');
// // 将脚本元素添加到页面中的 <head> 元素或者其他适当的位置
//         (document.head || document.documentElement).appendChild(script);
    //     console.log("Tab URL changed to: " + info.url);
    //     chrome.scripting.executeScript({
    //         target: {tabId: tab.id},
    //         files: ['content-script.js']
    //     });
    // }
    // chrome.scripting.executeScript({
    //     target: {tabId: tabId},
    //     files: ['contzent-script.js']
    // });


    // if (info.status === 'complete') {
    // console.log("chufahanhus")
    // chrome.scripting.executeScript({
    //     target: {tabId: tabId},
    //     function: clickElement,
    //     world: "MAIN",
    // });
    if (!tab.url) return;
    const url = new URL(tab.url);
    // siderPanelPath = "sidepanel.html"
    if (url.origin.search(GOOGLE_ORIGIN) != -1) {
        await chrome.sidePanel.setOptions({
            tabId,
            path: "sidepanel.html",
            // enabled: true
        });
    } else {
        await chrome.sidePanel.setOptions({
            tabId,
            enabled: false
        });
    }
});


// 接收消息
chrome.runtime.onMessage.addListener(async (message, sender) => {
    // siderPanelPath = "mainsidepanel.html"

    // (async () => {
    console.log("service-worker", message)
    if (message.type === 'open_side_panel') {
        siderPanelPath = "sidepanel.html"
        let url = ""
        let id = ""

        chrome.sidePanel.setOptions({
            tabId: sender.tab.id,
            path: "sidepanel.html",
            // enabled: true,
        });
        await chrome.sidePanel.open({tabId: sender.tab.id});
        // siderPanelPath = "mainsidepanel.html"
        // await chrome.sidePanel.setOptions({
        //     tabId: sender.tab.id,
        //     path: siderPanelPath,
        //     enabled: true,
        // });
        // 获取当前显示页面信息

        // (async () => {
        let [tab] = await chrome.tabs.query({active: true, currentWindow: true})
        // url = tab.url
        id = tab.id
        // // return {id: tab.id, url: tab.url}
        // // })()
        // console.log("当前页面信息", url, id)
        // chrome.runtime.sendMessage({type: "get_url", data: url})
        // console.log("请求后端")
        // url = message.data
        // let repo = url.replace("https://github.com/")

        // let url = request.data;

        // fetch("http://8.218.90.105:8790/plugine/repo_analyzer?type=GitHub&repo=kuafuai/DevOpsGPT", {
        //     method: "get"
        // }).then(res => {
        //     console.log("fetch then", res)
        // }).catch(err => {
        //     console.log("fetch err", err)
        // })
        // fetch(new Request())
        // 发送消息到content-script.js
        // TODO 修改
        // chrome.tabs.sendMessage(id, {type: "get_url", data: message.data})
        setTimeout(() => {
            chrome.runtime.sendMessage({type: 'action_analyzer', data: message.data});
        }, 100)
        // chrome.tabs.query({active: true, currentWindow: true})
        //chrome.tabs.sendMessage(sender.tab.id, "aadf")
    }
    // })();
});