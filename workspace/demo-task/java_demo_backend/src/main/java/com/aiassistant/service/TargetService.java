package com.aiassistant.service;

import com.aiassistant.model.Target;
import com.aiassistant.utils.ResultModel;
import com.aiassistant.utils.ResultPageModel;

/**
 * 业务逻辑层--目标Service
 */
public interface TargetService {

    /**
     * 添加一条目标
     *
     * @param target
     */
    ResultModel<Target> addTarget(Target target);

    /**
     * 获取所有目标
     *
     * @return
     */
    ResultPageModel<Target> getTargetList();

    /**
     * 根据Id查询目标
     *
     * @param id
     * @return
     */
    Target getById(Integer id);
}