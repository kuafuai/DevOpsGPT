package com.aiassistant.controller;

import com.aiassistant.model.Target;
import com.aiassistant.service.TargetService;
import com.aiassistant.utils.ResultModel;
import com.aiassistant.utils.ResultPageModel;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

/**
 * 控制器层--目标Controller
 */
@RestController
@RequiredArgsConstructor
@Api(tags = "TargetController")
public class TargetController {

    private final TargetService targetService;

    @PostMapping("/addTarget")
    @ApiOperation(value = "Add a new target")
    public ResultModel addTarget(@RequestBody Target target) {
        return targetService.addTarget(target);
    }

    @GetMapping("/getTargetList")
    @ApiOperation(value = "Get target list")
    public ResultPageModel<Target> getTargetList() {
        return targetService.getTargetList();
    }
}