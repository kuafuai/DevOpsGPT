package com.aiassistant.model;

import lombok.Data;

/**
 * 实体类--用户信息
 */
@Data
public class UserModel {
    private String userNiceName;
    private String userEmail;
    private String userUrl;
    private Integer userStatus;
    private String displayName;
}
