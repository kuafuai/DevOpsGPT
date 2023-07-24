package com.aiassistant.mapper;

import com.aiassistant.model.UserModel;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;
import java.util.Map;

/**
 * 持久化层--用户Mapper
 */
@Mapper
public interface UserMapper {

    /**
     * 查询最新一条用户记录
     *
     * @return
     */
    Map<String, Object> selectOne();

    /**
     * 查询所有用户记录
     *
     * @return
     */
    List<UserModel> selectAll();
}
