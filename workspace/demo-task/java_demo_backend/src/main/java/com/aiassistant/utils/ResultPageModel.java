package com.aiassistant.utils;

import java.util.Collections;
import java.util.List;

/**
 * 控制层-对外返回列表数据结构
 *
 * @param <T>
 */
public class ResultPageModel<T> {

    private Integer totalRecords = 0;
    private Integer pageNo = 1;
    private Integer pageSize = 10;
    private Integer totalPage = 0;

    private transient Integer firstIndex;

    public Integer getFirstIndex() {
        return firstIndex;
    }

    private List<T> list;

    /**
     * 创建列表返回
     *
     * @param list
     * @param <T>
     * @return
     */
    public static <T> ResultPageModel<T> of(List<T> list) {
        ResultPageModel<T> resultPageModel = new ResultPageModel<>(1, list.size());
        resultPageModel.setTotalRecords(list.size());
        resultPageModel.setList(list);
        return resultPageModel;
    }

    public ResultPageModel(Integer pageNo, Integer pageSize) {
        if (pageNo == null || pageNo < 1) {
            pageNo = 1;
        }
        if (pageSize == null || pageSize < 10) {
            pageSize = 10;
        }
        this.pageNo = pageNo;
        this.pageSize = pageSize;
        this.list = Collections.emptyList();
        this.firstIndex = (pageNo - 1) * pageSize;
    }

    public Integer getTotalRecords() {
        return totalRecords;
    }

    public void setTotalRecords(Integer count) {
        this.totalRecords = count;
        if (totalRecords != 0) {
            if (totalRecords % pageSize == 0) {
                totalPage = totalRecords / pageSize;
            } else {
                totalPage = totalRecords / pageSize + 1;
            }
        }
    }

    public Integer getPageNo() {
        return pageNo;
    }

    public void setPageNo(Integer pageNumber) {
        if (pageNumber < 1) {
            pageNumber = 1;
        }
        this.pageNo = pageNumber;
    }

    public Integer getPageSize() {
        return pageSize;
    }

    public void setPageSize(Integer pageSize) {
        if (pageSize < 1) {
            pageSize = 1;
        }
        this.pageSize = pageSize;
    }

    public List<T> getList() {
        return list;
    }

    public void setList(List<T> list) {
        this.list = list;
    }

    public Integer getTotalPage() {
        return totalPage;
    }

    public void setTotalPage(Integer totalPage) {
        this.totalPage = totalPage;
    }

}
