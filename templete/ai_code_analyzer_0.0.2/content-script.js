// let  title=document.querySelector("#repository-container-header > div.d-flex.flex-wrap.flex-justify-end.mb-3.container-xl.px-3.px-md-4.px-lg-5 > div.flex-auto.min-width-0.width-fit.mr-3 > div.d-flex.flex-wrap.flex-items-center.wb-break-word.f3.text-normal > span.Label.Label--secondary.v-align-middle.mr-1.d-none.d-md-block")

// const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay))
// 停止的函数
// const repeatedGreetings = async () => {
//     await sleep(1000)
//     // console.log(1)
//     // await sleep(1000)
//     // // console.log(2)
//     // await sleep(1000)
//     // console.log(3)
// }
// repeatedGreetings()
console.log("content-script")

function getButton() {
    // var  html="<button class='contentbutton'>AI Analyze</button>"
    // // var old="<button class=\"UnderlineNav-item no-wrap js-responsive-underlinenav-item js-selected-navigation-item\"><svg aria-hidden=\"true\" height=\"16\" viewBox=\"0 0 16 16\" version=\"1.1\" width=\"16\" data-view-component=\"true\" class=\"octicon octicon-play UnderlineNav-octicon d-none d-sm-inline\"><path d=\"M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm4.879-2.773 4.264 2.559a.25.25 0 0 1 0 .428l-4.264 2.559A.25.25 0 0 1 6 10.559V5.442a.25.25 0 0 1 .379-.215Z\"></path></svg></button>"
    // return new DOMParser().parseFromString(
    //     html,
    //     'text/html'
    // ).body.firstElementChild;

    let button = document.createElement("button");
    button.innerText = "AI Analysis"
    button.className = "AI-Analysis"
    // button.style.backgroundColor = "#4CAF50";
    button.style.backgroundColor = "#238636";
    button.style.border = "none";
    button.style.color = "white";
    button.style.padding = "4px 4px";
    button.style.textAlign = "center";
    button.style.textDecoration = "none";
    button.style.display = "inline-block";
    button.style.fontSize = "12px";
    button.style.fontWeight = "bold"
    button.style.margin = "4px 3px";
    button.style.transitionDuration = "0.4s";
    button.style.cursor = "pointer";
    button.style.borderRadius = "12px";
    return button
}

function addElement() {

    if (document.querySelectorAll("button.AI-Analysis").length === 0) {


        const title = document.querySelector('.d-flex.flex-wrap.flex-items-center.wb-break-word.f3.text-normal')
        /**
         * 生成分析的按钮
         * @returns {Element}
         */

        if (title) {
            // console.log("add BUTTON")
            const button = getButton();
            ``
            button.addEventListener('click', () => {
                // console.log("click button")
                let aelement = title.querySelector("#repository-container-header > div.d-flex.flex-wrap.flex-justify-end.mb-3.px-3.px-md-4.px-lg-5 > div.flex-auto.min-width-0.width-fit.mr-3 > div > strong > a");
                let url = aelement.href
                // console.log("content-script url", url)
                // chrome.runtime.sendMessage({type: 'open_side_panel'});
                chrome.runtime.sendMessage({type: 'open_side_panel', data: url});
                // 获取网址，发送给侧边栏
                // let [tab] = await chrome.tabs.query({active: true, currentWindow: true})

                // 延时发送第二条消息
                // setTimeout(() => {
                //     chrome.runtime.sendMessage({type: 'action_analyzer', data: tab.url});
                // }, 500)

            });
            // chrome.scripting.insertCSS("css/Content_Button.css")
            title.appendChild(button);
            // chrome.extension.
        }


        let organizationList = document.querySelector("#org-repositories > div > div > ul");
// 如果organization存在
        if (organizationList) {
            let childNodes = organizationList.querySelectorAll("li");
            if (childNodes) {
                for (var organiza of childNodes) {
                    //获取div
                    let divelement = organiza.querySelector("div > div.d-flex.flex-justify-between > div.mb-1.flex-auto");
                    // organiza
                    let button = getButton()
                    //获取span标签
                    let span = divelement.querySelector("span");

                    // let button = new DOMParser().parseFromString(
                    //     '<button class="UnderlineNav-item no-wrap js-responsive-underlinenav-item js-selected-navigation-item"><svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-play UnderlineNav-octicon d-none d-sm-inline"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm4.879-2.773 4.264 2.559a.25.25 0 0 1 0 .428l-4.264 2.559A.25.25 0 0 1 6 10.559V5.442a.25.25 0 0 1 .379-.215Z"></path></svg></button>',
                    //     'text/html'
                    // ).body.firstElementChild;

                    // 获取a标签中的路径
                    // console.log("add clickEvent")
                    button.addEventListener('click', () => {
                        // console.log("click button")
                        let aelement = divelement.querySelector("a");
                        let url = aelement.href
                        // console.log("content-script url", url)
                        chrome.runtime.sendMessage({type: 'open_side_panel', data: url});

                        // 获取网址，发送给侧边栏
                        // let [tab] = await chrome.tabs.query({active: true, currentWindow: true})

                        // 延时发送第二条消息
                        // setTimeout(() => {
                        //     chrome.runtime.sendMessage({type: 'action_analyzer', data: tab.url});
                        // }, 500)
                    });
                    span.after(button)

                    // var observer = new MutationObserver(function(mutations) {
                    //     mutations.forEach(function(mutation) {
                    //         if (mutation.type === 'childList') {
                    //             // 重新绑定按钮点击事件
                    //             if (myButton) {
                    //                 myButton.onclick = function() {
                    //                     console.log('Button clicked!');
                    //                 };
                    //             }
                    //         }
                    //     });
                    // });
                    //
                    // var config = { attributes: true, childList: true, subtree: true };
                    // var targetNode = document.body;
                    // observer.observe(targetNode, config);
                }
            }


        }

        let reposlist = document.querySelector("#org-repositories > div > div > div.Box > ul");
// 如果organization存在
        if (reposlist) {
            let childNodes = reposlist.querySelectorAll("li");
            if (childNodes) {
                for (var repo of childNodes) {
                    //获取div
                    let divelement = repo.querySelector("div > div.d-flex.flex-justify-between > div.flex-auto");
                    // organiza
                    let button = getButton()
                    //获取span标签
                    let span = divelement.querySelector("span");

                    // let button = new DOMParser().parseFromString(
                    //     '<button class="UnderlineNav-item no-wrap js-responsive-underlinenav-item js-selected-navigation-item"><svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-play UnderlineNav-octicon d-none d-sm-inline"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm4.879-2.773 4.264 2.559a.25.25 0 0 1 0 .428l-4.264 2.559A.25.25 0 0 1 6 10.559V5.442a.25.25 0 0 1 .379-.215Z"></path></svg></button>',
                    //     'text/html'
                    // ).body.firstElementChild;

                    // 获取a标签中的路径
                    // console.log("add clickEvent")
                    button.addEventListener('click', () => {
                        // console.log("click button")
                        let aelement = divelement.querySelector("a");
                        let url = aelement.href
                        // console.log("content-script url", url)
                        chrome.runtime.sendMessage({type: 'open_side_panel', data: url});

                        // 获取网址，发送给侧边栏
                        // let [tab] = await chrome.tabs.query({active: true, currentWindow: true})

                        // 延时发送第二条消息
                        // setTimeout(() => {
                        //     chrome.runtime.sendMessage({type: 'action_analyzer', data: tab.url});
                        // }, 500)
                    });
                    span.after(button)

                    // var observer = new MutationObserver(function(mutations) {
                    //     mutations.forEach(function(mutation) {
                    //         if (mutation.type === 'childList') {
                    //             // 重新绑定按钮点击事件
                    //             if (myButton) {
                    //                 myButton.onclick = function() {
                    //                     console.log('Button clicked!');
                    //                 };
                    //             }
                    //         }
                    //     });
                    // });
                    //
                    // var config = { attributes: true, childList: true, subtree: true };
                    // var targetNode = document.body;
                    // observer.observe(targetNode, config);
                }
            }


        }


        let olList = document.querySelector("body > div.logged-out.env-production.page-responsive > div.application-main > main > div > div > div > div.flex-shrink-0.col-12.col-md-9.mb-4.mb-md-0 > div > div > div.js-pinned-items-reorder-container > ol");
        if (olList) {
            let liList = olList.querySelectorAll("li");
            if (liList) {

                for (var li of liList) {
                    //    获取github项目地址

                    let aiButton = getButton();
                    // 添加点击事件
                    // console.log("add clickEvent")
                    aiButton.addEventListener('click', () => {
                        // console.log("click button")
                        let divelement = li.querySelector(" div > div > div > div")
                        let aelement = divelement.querySelector("a")
                        // let url = aelement.href
                        let url = aelement.href
                        // console.log("content-script url", url)
                        // chrome.runtime.sendMessage({type: 'open_side_panel'});
                        chrome.runtime.sendMessage({type: 'open_side_panel', data: url});
                        // 获取网址，发送给侧边栏
                        // let [tab] = await chrome.tabs.query({active: true, currentWindow: true})

                        // 延时发送第二条消息
                        // setTimeout(() => {
                        //     chrome.runtime.sendMessage({type: 'action_analyzer', data: tab.url});
                        // }, 500)
                    });
                    // 将button元素添加到页面中
                    var spanElement = li.querySelector("div > div > div > div > span.Label.Label--secondary.v-align-middle.mt-1.no-wrap.v-align-baseline.Label--inline")
                    spanElement.after(aiButton)
                }
            }
        }


//  https://github.com/trending
        let trendingelement = document.querySelectorAll("body > div.logged-in.env-production.page-responsive > div.application-main > main > div.position-relative.container-lg.p-responsive.pt-6 > div > div:nth-child(2) > article > h2.h3.lh-condensed")
        if (trendingelement) {
            for (var divelement of trendingelement) {
                let trendButton = getButton();
                let aelement = divelement.querySelector("a.Link");
                // console.log("add clickEvent")
                trendButton.addEventListener('click', () => {
                    // console.log("click button")
                    let url = aelement.href;
                    // console.log("content-script url", url)
                    // chrome.runtime.sendMessage({type: 'open_side_panel'});
                    chrome.runtime.sendMessage({type: 'open_side_panel', data: url});
                    // 获取网址，发送给侧边栏
                    // let [tab] = await chrome.tabs.query({active: true, currentWindow: true})

                    // 延时发送第二条消息
                    // setTimeout(() => {
                    //     chrome.runtime.sendMessage({type: 'action_analyzer', data: tab.url});
                    // }, 500)
                })
                aelement.after(trendButton)
            }

        }
    }
}

// let buttonList = document.querySelectorAll("button.AI-Analysis");
if (document.querySelectorAll("button.AI-Analysis").length === 0) {
    // console.log("add element")
   setTimeout(()=>{
       addElement()
   },1000)
}
// else {
//     console.log("remove child")
//     var list = document.querySelectorAll("button.AI-Analysis")
//
//     // 添加元素
//     setTimeout(() => {
//         console.log("content settimout")
//         if (list != null) {
//             console.log("删除 button")
//             for (var buttonitem of list) {
//                 if (buttonitem.parentNode != null) {
//                     console.log("删除 button parent")
//                     buttonitem.parentNode.removeChild(buttonitem)
//                 }
//             }
//         }
//
//         setTimeout(() => {
//             console.log("add button timeout")
//             addElement()
//         }, 1000)
//     }, 3000)
//
//
//     // setTimeout(()=>{
//     //     addElement()
//     // },3000)
// }
chrome.runtime.onMessage.addListener(function (request, sender, send) {
    // 如果消息类型为获取url路径，那么再发送消息
    if (request.type === "get_url") {
        // console.log("content-script get_url", request)
        // let url = request.data;
        //  发送消息到侧边栏，展示页面信息
        // chrome.runtime.sendMessage({type: 'action_analyzer', data: url},);
        // 延时发送第二条消息
        // setTimeout(() => {
        //     chrome.runtime.sendMessage({type: 'action_analyzer', data: url});
        // }, 100)
    }
    // else if (request.type === "test") {
    //     // console.log("content-script test message", request.data)
    //
    //     // 如果为空则注入
    //     // if (buttonList == null) {
    //     //
    //     // }
    // }
    // console.log(request, sender)
});
// setTimeout(()=>{


// },3000)

// 接收消息
