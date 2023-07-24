package com.aiassistant.utils;

import lombok.Data;

/**
 * 控制层-对外返回数据结构
 *
 * @param <T>
 */
@Data
public class ResultModel<T> {

    private Exception exception = null;
    private T data = null;
    private String msg;
    private Integer code;

    public static <T> ResultModel ofResult(Integer code, String msg, T data) {
        return ofResult(code, msg, data, null);
    }

    public static <T> ResultModel ofResult(Integer code, String msg, T data, Exception exception) {
        ResultModel<T> resultModel = new ResultModel();
        resultModel.setCode(code);
        resultModel.setData(data);
        resultModel.setMsg(msg);
        resultModel.setException(exception);
        return resultModel;
    }

    /**
     * 创建成功返回
     *
     * @return
     */
    public static ResultModel ofSuccess() {

        return ofSuccess(null);
    }

    /**
     * 创建成功返回-带返回数据
     *
     * @param data
     * @param <T>
     * @return
     */
    public static <T> ResultModel ofSuccess(T data) {

        return ofSuccess(null, data);
    }

    /**
     * 创建成功返回-带返回信息和返回数据
     *
     * @param msg
     * @param data
     * @param <T>
     * @return
     */
    public static <T> ResultModel ofSuccess(String msg, T data) {

        return ofResult(0, msg, data);
    }

    /**
     * 创建失败返回
     *
     * @return
     */
    public static ResultModel ofError() {

        return ofError(null);
    }

    /**
     * 创建失败返回-带返回信息
     *
     * @param msg
     * @return
     */
    public static ResultModel ofError(String msg) {

        return ofError(msg, null);
    }

    public static ResultModel ofError(String msg, Exception exception) {

        return ofResult(999, msg, null, exception);
    }
}
