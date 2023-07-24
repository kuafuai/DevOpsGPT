package com.aiassistant.utils;

import lombok.experimental.UtilityClass;

@UtilityClass
public class StringUtils {

    /**
     * 判断字符串是否为空
     *
     * @param var
     * @return
     */
    public static boolean isEmpty(String var) {
        return org.apache.commons.lang3.StringUtils.isEmpty(var);
    }
}
