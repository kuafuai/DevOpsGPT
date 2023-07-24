package com.aiassistant.mapper;

import com.aiassistant.model.Target;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

/**
 * 持久化层--目标Mapper
 */
@Mapper
public interface TargetMapper {

    /**
     * 插入一条目录记录
     *
     * @param target
     */
    Target insertTarget(Target target);

    /**
     * 查询所有目录记录
     *
     * @return
     */
    List<Target> getTargetList();

    /**
     * 根据Id查询目标
     *
     * @param id
     * @return
     */
    Target selectById(@Param("id") Integer id);
}