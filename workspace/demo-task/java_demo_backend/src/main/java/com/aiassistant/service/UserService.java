package com.aiassistant.service;

import com.aiassistant.model.UserModel;

import java.util.List;


/**
 * 业务逻辑层--用户Service
 */
public interface UserService {

    /**
     * 查询所有用户
     *
     * @return
     */
    List<UserModel> queryAll();
}
