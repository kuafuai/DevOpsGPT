package com.aiassistant.service.impl;

import com.aiassistant.mapper.TargetMapper;
import com.aiassistant.model.Target;
import com.aiassistant.service.TargetService;
import com.aiassistant.utils.ResultModel;
import com.aiassistant.utils.ResultPageModel;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * 业务逻辑层--目标Service接口实现
 */
@Service
@RequiredArgsConstructor
public class TargetServiceImpl implements TargetService {

    private final TargetMapper targetMapper;

    @Override
    public ResultModel<Target> addTarget(Target target) {
        Target result = targetMapper.insertTarget(target);
        return ResultModel.ofSuccess(result);
    }

    @Override
    public ResultPageModel<Target> getTargetList() {
        List<Target> list = targetMapper.getTargetList();

        return ResultPageModel.of(list);
    }


    @Override
    public Target getById(Integer id) {
        return targetMapper.selectById(id);
    }
}