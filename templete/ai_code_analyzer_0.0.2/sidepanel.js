// console.log(11122);
// console.log(window.location.toString)
// console.log(window.location.href)
//
async function getCurrentTab() {
    const queryOptions = {active: true, currentWindow: true};
    const [tab] = await chrome.tabs.query(queryOptions);
    return tab;
}

// console.log(1111111)
/**
 * 是否显示加载中,
 * isShow为false 显示加载中
 * true：显示分析内容
 */
var isShow = false // 是否显示加载中
function updateLoad() {
    // $("#mainsidepanel").css({
    //     "display": "none"
    // })
    // $("#sidepanel").css({
    //     "display": "block"
    // })
    // 错误提示框与加载中以及分析结果展示框都是互斥的


    if (isShow) {
        $("#contentId").css({
            "display": "block"
        })
        $("#loadId").css({
            "display": "none"
        })
        let footer = $(".footer");
        footer.css({
            position: "",
            bottom: ""
        })
    } else {
        $("#error").css({
            display: "none"
        })
        $(".footer").css({
            "position": "absolute",
            "bottom": "0"
        })
        $("#contentId").css({
            "display": "none"
        })
        $("#loadId").css({
            "display": "block"
        })

    }
}

function updateError(message) {
    $("#mainsidepanel").css({
        "display": "none"
    })
    $("#sidepanel").css({
        "display": "block"
    })

    //    隐藏加载中的效果
    $("#loadId").css({
        "display": "none"
    })
    $("#contentId").css({
        "display": "none"
    })
    // 显示错误提示
    if (message !== null && message !== "" && message !== undefined) {
        $("#errmessage").html(message)
    } else {
        $("#errmessage").html("Unknown error")
    }
    $("#error").css({
        "display": "block"
    })
    $(".footer").css({
        "position": "absolute",
        "bottom": "0"
    })
}

// updateLoad()


// 获取待展示信息的domo节点
let language = $("#language");
let framework = $("#framework");
let module = $("#module");
let usage = $("#usage");
let code = $("#code");


// let repo = ""
/**
 * 发送请求的函数
 */
// $("#sendrequest").click(() => {
//     console.log("button被触发")
//     // let url = "http://8.218.90.105:8790/plugine/repo_analyzer?type=GitHub&repo=kuafuai/DevOpsGPT"
//     // var url = "http://192.168.137.1:8790/test"
//     // var url = "http://114.116.233.39:8790/test"
//     // console.log("siderpanel repo", repo)
//     if (isShow) {
//         isShow = false
//     } else {
//         isShow = true
//     }
//     updateLoad()
//     let type = ""
//     // $.ajax({
//     //     type: "GET",
//     //     url: url,
//     //     timeout: 900000,
//     //     success: function (res) {
//     //         console.log("network success", res);
//     //     },
//     //     error: function (err) {
//     //         console.log("network error", err)
//     //     }
//     // });
//
//     // const controller = new AbortController();
//     // const signal = controller.signal;
//     //
//     // const timeoutId = setTimeout(() => {
//     //     controller.abort();
//     //     console.log("sidepanel 请求超时");
//     //     // 可以在此处添加处理超时的代码
//     // }, 900000); // 设置超时时间为15分钟，以毫秒为单位
//     //
//     // fetch(url, {signal})
//     //     .then(response => {
//     //         if (response.ok) {
//     //             clearTimeout(timeoutId); // 在请求成功时清除超时计时器
//     //             // console.log("success",response.json())
//     //             return response.json();
//     //         } else {
//     //             console.log("sidepanel 发生错误", response)
//     //         }
//     //
//     //     })
//     //     .then(data => {
//     //         console.log("sidepanel success", data);
//     //         // 处理返回的数据
//     //     })
//     //     .catch(error => {
//     //         if (error.name === 'AbortError') {
//     //             console.log('sidepanel 请求被中止');
//     //             // 可以在此处添加处理请求被中止的代码
//     //         } else {
//     //             console.error('sidepanel 发生错误', error);
//     //             // 可以在此处添加处理其他错误的代码
//     //         }
//     //     });
// })

var trimer
/**
 * 发送网络请求，异步获取数据
 * @returns {Promise<void>}
 */
let task_no = ""
/**
 * 定时获取请求内容
 * @returns {Promise<void>}
 */
// let res = {
//     data: {
//         "message": "分析代码中",
//         "status": 1,
//         "task_no": "5c81cf9c01186f8669380b9d8accee46"
//     },
//     success: true
// }
getContentByTask = async () => {
    if (trimer) {
        clearTimeout(trimer)
        trimer = null
    }

    try {
        // let url = "http://localhost:8790/test";
        // let url = "http://8.218.90.105:8790/plugine/repo_analyzer_check?task_no=" + task_no;
        let url = "https://www.kuafuai.net/backend/plugine/repo_analyzer_check?task_no=" + task_no;
        let res = await $.get(url)
        // res = {
        //     data: {
        //         "message": "{'name': 'python_project_function_summary', 'git_config_id': 0, 'ci_config_id': 0, 'cd_config_id': 0, 'cd_container_name': '', 'cd_container_group': '', 'cd_region': '', 'cd_public_ip': '', 'cd_security_group': '', 'cd_subnet': '', 'git_path': 'kuafuai/DevOpsGPT', 'git_workflow': 'default.yaml', 'role': '该项目提供了多个控制器，包括后端应用控制器、支付处理控制器、需求处理控制器、设置处理控制器、接口文档生成控制器、代码处理控制器、DevOps处理控制器、需求处理控制器、子任务处理控制器、租户处理控制器、用户处理控制器和工作空间处理控制器。每个控制器都提供了不同的功能，包括添加、获取、分析、获取价格、创建支付、退款、取消支付、支付验证、订单支付、续费、充值、清理、设置应用、更新、获取配置列表、编辑配置、生成接口文档、编辑文件任务、检查文件、合并文件、引用修复、修复编译、修复Lint、触发CI、插件CI、检查编译、检查Lint、触发CD、澄清、分析、创建租户、获取成员、使用租户、邀请、获取账单、注册、登录、注销、更改语言、更改密码、发送启动代码、保存代码、创建工作空间、Git推送和重置工作空间。', 'struct_cache': '对外服务接口: backend.app.controllers.app : 后端应用控制器\\n  提供功能: add : 添加\\n  提供功能: getAll : 获取所有\\n  提供功能: get_tpl : 获取模板\\n  提供功能: analyze_service : 分析服务\\n对外服务接口: backend.app.controllers.pay_pro : 支付处理控制器\\n  提供功能: get_price : 获取价格\\n  提供功能: create_pay : 创建支付\\n  提供功能: return_pay : 退款\\n  提供功能: cancel_pay : 取消支付\\n  提供功能: checkPaymentAli : 支付宝支付验证\\n  提供功能: checkPaymentPayPal : PayPal支付验证\\n  提供功能: orderPayPal : PayPal订单支付\\n  提供功能: orderAli : 支付宝订单支付\\n  提供功能: Renew : 续费\\n  提供功能: Recharge : 充值\\n对外服务接口: backend.app.controllers.requirement : 需求处理控制器\\n  提供功能: clear_up : 清理\\n  提供功能: setup_app : 设置应用\\n  提供功能: get_all : 获取所有\\n  提供功能: get_one : 获取一个\\n  提供功能: update : 更新\\n对外服务接口: backend.app.controllers.setting : 设置处理控制器\\n  提供功能: get_git_config_list : 获取Git配置列表\\n  提供功能: get_ci_config_list : 获取CI配置列表\\n  提供功能: get_cd_config_list : 获取CD配置列表\\n  提供功能: get_llm_config_list : 获取LLM配置列表\\n  提供功能: edit_git : 编辑Git配置\\n  提供功能: edit_ci : 编辑CI配置\\n  提供功能: edit_cd : 编辑CD配置\\n对外服务接口: backend.app.controllers.step_api : 接口文档生成控制器\\n  提供功能: gen_interface_doc : 生成接口文档\\n对外服务接口: backend.app.controllers.step_code : 代码处理控制器\\n  提供功能: edit_file_task : 编辑文件任务\\n  提供功能: check_file : 检查文件\\n  提供功能: merge_file : 合并文件\\n  提供功能: reference_repair : 引用修复\\n  提供功能: fix_compile : 修复编译\\n  提供功能: fix_lint : 修复Lint\\n对外服务接口: backend.app.controllers.step_devops : DevOps处理控制器\\n  提供功能: trigger_ci : 触发CI\\n  提供功能: plugin_ci : 插件CI\\n  提供功能: check_compile : 检查编译\\n  提供功能: check_lint : 检查Lint\\n  提供功能: trigger_cd : 触发CD\\n对外服务接口: backend.app.controllers.step_requirement : 需求处理控制器\\n  提供功能: clarify : 澄清\\n对外服务接口: backend.app.controllers.step_subtask : 子任务处理控制器\\n  提供功能: analysis : 分析\\n对外服务接口: backend.app.controllers.tenant_pro : 租户处理控制器\\n  提供功能: create : 创建\\n  提供功能: get_all : 获取所有\\n  提供功能: get_one : 获取一个\\n  提供功能: get_members : 获取成员\\n  提供功能: use_tenant : 使用租户\\n  提供功能: invite : 邀请\\n  提供功能: get_billings : 获取账单\\n对外服务接口: backend.app.controllers.user : 用户处理控制器\\n  提供功能: register : 注册\\n  提供功能: login : 登录\\n  提供功能: logout : 注销\\n  提供功能: change_language : 更改语言\\n  提供功能: changepassword : 更改密码\\n  提供功能: language : 语言\\n  提供功能: send_launch_code : 发送启动代码\\n对外服务接口: backend.app.controllers.workspace : 工作空间处理控制器\\n  提供功能: save_code : 保存代码\\n  提供功能: create : 创建\\n  提供功能: gitpush : Git推送\\n  提供功能: resetWorkspace : 重置工作空间', 'language': 'Python', 'framework': 'Flask+SQLAlchemy', 'database': '信息不足', 'api_type': 'swagger', 'api_location': '', 'service_libs_name': 'flask-sqlalchemy,flask-cors,pyyaml,python-gitlab,openai,aliyun-python-sdk-core,aliyun-python-sdk-eci,alembic,paypalrestsdk,alipay-sdk-python,SQLAlchemy'}",
        //         "status": 2,
        //         "task_no": "5c81cf9c01186f8669380b9d8accee46"
        //     },
        //     success: true
        // }
        // let res = {
        //     data: {
        //         "message": "init task",
        //         "status": 1,
        //         "task_no": "5c81cf9c01186f8669380b9d8accee46"
        //     },
        //     success: true
        // }


        // trimer = setTimeout(getAiContent, 1000)

        /**
         * {
  "data": {
        "message": "Init Task",
        "status": 0——初始化任务，1—— 处理中 2 —— 成功 3 ————失败
        "task_no": "0d39d3ed57cd65ee3481d884530965b8"
     },
  "success": true
}
         */
        // console.log("4444444444444444444")
        if (res.success) {
            // if (res.data.)
            if (res.data.status !== 2 && res.data.status !== 3) {

                console.log("sidepanel plugine/repo_analyzer_check handle success", res)
                // 修改提示语
                $("#loadcontent").text(res.data.message + "....")
                $(".footer").css({
                    "position": "absolute",
                    "bottom": "0"
                })
                // $("#error").css({
                //     display: "none"
                // })
                isShow = false
                updateLoad()
                // $(".loader").css({
                //     "border": "5px solid white", /* Light grey */
                //     "border-top": "3px solid #3498db", /* Blue */
                //     "border-radius": "50%",
                //     "width": "50px",
                //     "height": "50px",
                //     " animation": "spin 2s linear infinite",
                //     "margin-bottom": " 20px"
                // })
                trimer = setTimeout(getContentByTask, 5000)
                // setTimeout(() => {
                //     res = {
                //         data: {
                //             "message": "{'name': 'python_project_function_summary', 'git_config_id': 0, 'ci_config_id': 0, 'cd_config_id': 0, 'cd_container_name': '', 'cd_container_group': '', 'cd_region': '', 'cd_public_ip': '', 'cd_security_group': '', 'cd_subnet': '', 'git_path': 'kuafuai/DevOpsGPT', 'git_workflow': 'default.yaml', 'role': '该项目提供了多个控制器，包括后端应用控制器、支付处理控制器、需求处理控制器、设置处理控制器、接口文档生成控制器、代码处理控制器、DevOps处理控制器、需求处理控制器、子任务处理控制器、租户处理控制器、用户处理控制器和工作空间处理控制器。每个控制器都提供了不同的功能，包括添加、获取、分析、获取价格、创建支付、退款、取消支付、支付验证、订单支付、续费、充值、清理、设置应用、更新、获取配置列表、编辑配置、生成接口文档、编辑文件任务、检查文件、合并文件、引用修复、修复编译、修复Lint、触发CI、插件CI、检查编译、检查Lint、触发CD、澄清、分析、创建租户、获取成员、使用租户、邀请、获取账单、注册、登录、注销、更改语言、更改密码、发送启动代码、保存代码、创建工作空间、Git推送和重置工作空间。', 'struct_cache': '对外服务接口: backend.app.controllers.app : 后端应用控制器\\n  提供功能: add : 添加\\n  提供功能: getAll : 获取所有\\n  提供功能: get_tpl : 获取模板\\n  提供功能: analyze_service : 分析服务\\n对外服务接口: backend.app.controllers.pay_pro : 支付处理控制器\\n  提供功能: get_price : 获取价格\\n  提供功能: create_pay : 创建支付\\n  提供功能: return_pay : 退款\\n  提供功能: cancel_pay : 取消支付\\n  提供功能: checkPaymentAli : 支付宝支付验证\\n  提供功能: checkPaymentPayPal : PayPal支付验证\\n  提供功能: orderPayPal : PayPal订单支付\\n  提供功能: orderAli : 支付宝订单支付\\n  提供功能: Renew : 续费\\n  提供功能: Recharge : 充值\\n对外服务接口: backend.app.controllers.requirement : 需求处理控制器\\n  提供功能: clear_up : 清理\\n  提供功能: setup_app : 设置应用\\n  提供功能: get_all : 获取所有\\n  提供功能: get_one : 获取一个\\n  提供功能: update : 更新\\n对外服务接口: backend.app.controllers.setting : 设置处理控制器\\n  提供功能: get_git_config_list : 获取Git配置列表\\n  提供功能: get_ci_config_list : 获取CI配置列表\\n  提供功能: get_cd_config_list : 获取CD配置列表\\n  提供功能: get_llm_config_list : 获取LLM配置列表\\n  提供功能: edit_git : 编辑Git配置\\n  提供功能: edit_ci : 编辑CI配置\\n  提供功能: edit_cd : 编辑CD配置\\n对外服务接口: backend.app.controllers.step_api : 接口文档生成控制器\\n  提供功能: gen_interface_doc : 生成接口文档\\n对外服务接口: backend.app.controllers.step_code : 代码处理控制器\\n  提供功能: edit_file_task : 编辑文件任务\\n  提供功能: check_file : 检查文件\\n  提供功能: merge_file : 合并文件\\n  提供功能: reference_repair : 引用修复\\n  提供功能: fix_compile : 修复编译\\n  提供功能: fix_lint : 修复Lint\\n对外服务接口: backend.app.controllers.step_devops : DevOps处理控制器\\n  提供功能: trigger_ci : 触发CI\\n  提供功能: plugin_ci : 插件CI\\n  提供功能: check_compile : 检查编译\\n  提供功能: check_lint : 检查Lint\\n  提供功能: trigger_cd : 触发CD\\n对外服务接口: backend.app.controllers.step_requirement : 需求处理控制器\\n  提供功能: clarify : 澄清\\n对外服务接口: backend.app.controllers.step_subtask : 子任务处理控制器\\n  提供功能: analysis : 分析\\n对外服务接口: backend.app.controllers.tenant_pro : 租户处理控制器\\n  提供功能: create : 创建\\n  提供功能: get_all : 获取所有\\n  提供功能: get_one : 获取一个\\n  提供功能: get_members : 获取成员\\n  提供功能: use_tenant : 使用租户\\n  提供功能: invite : 邀请\\n  提供功能: get_billings : 获取账单\\n对外服务接口: backend.app.controllers.user : 用户处理控制器\\n  提供功能: register : 注册\\n  提供功能: login : 登录\\n  提供功能: logout : 注销\\n  提供功能: change_language : 更改语言\\n  提供功能: changepassword : 更改密码\\n  提供功能: language : 语言\\n  提供功能: send_launch_code : 发送启动代码\\n对外服务接口: backend.app.controllers.workspace : 工作空间处理控制器\\n  提供功能: save_code : 保存代码\\n  提供功能: create : 创建\\n  提供功能: gitpush : Git推送\\n  提供功能: resetWorkspace : 重置工作空间', 'language': 'Python', 'framework': 'Flask+SQLAlchemy', 'database': '信息不足', 'api_type': 'swagger', 'api_location': '', 'service_libs_name': 'flask-sqlalchemy,flask-cors,pyyaml,python-gitlab,openai,aliyun-python-sdk-core,aliyun-python-sdk-eci,alembic,paypalrestsdk,alipay-sdk-python,SQLAlchemy'}",
                //             "status": 2,
                //             "task_no": "5c81cf9c01186f8669380b9d8accee46"
                //         },
                //         success: true
                //     }
                // }, setTimeout(5000))
            } else {
                if (res.data.status === 2) {
                    // 在此处向页面中展示分析内容
                    let text = res.data.message.replaceAll("\'", "\"");
                    // console.log(text)
                    var result = JSON.parse(text)
                    if (result.language != null) {
                        language.html(result.language.replace(/ /g, "&nbsp;"))
                    } else {
                        language.html("")
                    }

                    if (result.framework != null) {
                        framework.html(result.framework.replace(/ /g, "&nbsp;"))
                    } else {
                        framework.html("")
                    }

                    if (result.role != null) {
                        usage.html(result.role.replace(/ /g, "&nbsp;"))
                    } else {
                        usage.html("")
                    }

                    if (result.struct_cache != null) {
                        code.html(result.struct_cache.replace(/ /g, "&nbsp;"))
                    } else {
                        code.html("")
                    }

                    if (result.service_libs_name != null) {
                        module.html(result.service_libs_name.replace(/ /g, "&nbsp;"))
                    } else {
                        module.html("")
                    }


                    // $(".footer").removeAttribute({
                    //     "position": "absolute",
                    //     "bottom": "0"
                    // })

                    let footer = $(".footer");
                    footer.css({
                        position: "",
                        bottom: ""
                    })
                    // footer.removeAttribute("bottom")
                    // $(".footer").removeAttribute("position")

                    // 显示结果
                    isShow = true
                    updateLoad()
                    console.log("sidepanel plugine/repo_analyzer_check finish success", "请求以处理完成", res)
                } else if (res.data.status === 3) {
                    let message = res.data.message;
                    updateError(message)
                    console.log("sidepanel plugine/repo_analyzer_check finish error", "请求以处理失败", res)
                }
            }
        } else {
            updateError(res.data.message)
            console.log("sidepanel plugine/repo_analyzer_check error", res.data.message)
        }

        // }
    } catch (e) {
        // 提示后端服务下线了
        updateError("The back-end service is offline")
        console.log("sidepanel plugine/repo_analyzer_check error", e)
    }
}

/**
 * 获取task_no 任务id
 * @returns {Promise<void>}
 */
let repo_name = "" // 仓库名称
getAiContent = async () => {
    clearTimeout(trimer)
    // if (trimer) {
    //     clearTimeout(trimer)
    //     trimer = null
    // }
    try {
        // let url = "http://localhost:8790/test";
        // let url = "http://8.218.90.105:8790/plugine/repo_analyzer?type=GitHub&repo=" + repo_name;
        let url = "https://www.kuafuai.net/backend/plugine/repo_analyzer?type=GitHub&repo=" + repo_name;
        // console.log(url)
        let res = await $.get(url)

        // let res = {
        //     success: true,
        //     data: {
        //         task_no: "111111"
        //     }
        // }
        // let number = Math.ceil(Math.random() * 10);
        // if (!(number % 2 === 0)) {
        // console.log(number)
        // trimer = setTimeout(getAiContent, 1000)
        // console.log("sidepanel  plugine/repo_analyze success", res)
        if (res.success) {
            // console.log("66666666666666666666")
            task_no = res.data.task_no
            // 保存任务id与reponame对应关系
            // await chrome.storage.sync.set({task_no, repo_name})
            // task_no = "e9490c82da75254ef991f5c0dbf709a9"
            getContentByTask()
        } else {
            // 显示错误提示框
            let message = res.data.message;
            // 如果 res.data 中有error_code 字段
            if (res.data.hasOwnProperty("error_code")) {
                if (res.data.error_code === 1001) {
                    if (repo_name === res.data.repo) {
                        task_no = res.data.task_no
                        getContentByTask()
                    } else {
                        // task_no = res.data.task_no
                        // let title = document.getElementById("title");
                        // title.innerText = res.data.repo
                        // getContentByTask()
                        // 缓存中没有这个任务id，直接展示“当前有其他任务处理中”
                        updateError(message + "<br><a href='#' id='conitnue'>" + "Continue to analyze " + res.data.repo + "</a>")
                        $("#conitnue").click(() => {
                            task_no = res.data.task_no
                            let title = document.getElementById("title");
                            title.innerText = res.data.repo
                            getContentByTask()
                        })
                    }
                } else if (res.data.error_code === 3001) {
                    updateError(message + "  website:<a href=\"https://www.kuafuai.net\" target=\"_blank\">KuaFuAI</a>")
                } else {
                    updateError(message)
                }
                //    获取缓存中的对应关系，如果任务id是当前的仓库对应的任务id，继续请求
                // let strorgeRepoName = await chrome.storage.sync.get([task_no]);

            } else {
                // 正常展示信息
                updateError(message)
            }

        }

        // }
    } catch (e) {
        updateError("The back-end service is offline")
        console.log("sidepanel plugine/repo_analyzer error", e)
    }
}

// 测试
// $("#test").click(() => {
//     // getAiContent()
// })

// setTimeout(()=>{
//     $("#loadcontent").text("分析lib组件....")
// },3000)
//
// setTimeout(()=>{
//     $("#loadcontent").text("分析代码....")
// },3000)

// 接收

chrome.runtime.onMessage.addListener(async (request, sender, sendResponse) => {
        // console.log("1111111111111111111111111111111111")
        // 隐藏错误提示框
        /**
         * 校验加载中效果
         */
        // setTimeout(() => {
        //     isShow = true
        //     updateLoad()
        // }, 3000)
        // console.log("sidepanel", request)
        if (request.type === 'action_analyzer') {
            console.log("sidepanel analyzer", request)
            // console.log("触发消息通知")
            $("#sidepanel").css({
                "display": "block"
            })
            $("#mainsidepanel").css({
                "display": "none"
            })
            $("#loadcontent").text("Loading....")
            $("#loadmessage").text("Estimated completion time 5-10 minutes")
            // 显示laoding
            isShow = false
            updateLoad()
            $("#error").css({
                "display": "none"
            })

            //    显示信息到侧边栏中
            let title = document.getElementById("title");
            let url = request.data;
            let repotemp = url.replace("https://github.com/", "")
            title.innerText = repotemp
            repo_name = repotemp
            // 如果获取仓库名称直接返回失败，不调用接口


            //  发送网络请求，不间断发送
            getAiContent()
            // getAiContent()
            // while (true) {


            // }

            // await chrome.storage.sync.set({"repo": repo})
            //
            // let result = await chrome.storage.sync.get(["repo"])
            // console.log("repo current value is ", result)
            // 设定仓库
            // repo = repotemp;


            // var url = "http://127.0.0.1:8790/test"
            // $.get(url, function (data, status) {
            //     console.log('Data: ' + data);
            //     console.log('Status: ' + status);
            // });
            // $.get(url).then(res => {
            //     console.log(res)
            // }).error(err => {
            //     console.log(err)
            // })
        }
    }
)
;
// window.onbeforeunload = function (e) {
//     // console.log("页面卸载事件")
//     // // 页面关闭时发送的消息
//     // e.preventDefault()
//     chrome.runtime.sendMessage({"type": "homepage", data: ""})
// }

// 监听数据的改变
// chrome.storage.sync.get