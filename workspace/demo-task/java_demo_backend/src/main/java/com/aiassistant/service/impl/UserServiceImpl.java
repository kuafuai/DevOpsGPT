package com.aiassistant.service.impl;

import com.aiassistant.mapper.UserMapper;
import com.aiassistant.model.UserModel;
import com.aiassistant.service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;


/**
 * 业务逻辑层--用户Service接口实现
 */
@Service
@RequiredArgsConstructor
public class UserServiceImpl implements UserService {

    private final UserMapper userMapper;

    @Override
    public List<UserModel> queryAll() {

        return userMapper.selectAll();
    }
}
