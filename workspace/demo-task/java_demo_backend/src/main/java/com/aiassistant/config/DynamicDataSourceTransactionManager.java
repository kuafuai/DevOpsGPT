package com.aiassistant.config;

import org.springframework.jdbc.datasource.DataSourceTransactionManager;
import org.springframework.transaction.TransactionDefinition;

import javax.sql.DataSource;

public class DynamicDataSourceTransactionManager extends DataSourceTransactionManager {


    public DynamicDataSourceTransactionManager(DataSource dataSource) {
        super(dataSource);
    }


    @Override
    protected void doBegin(Object transaction, TransactionDefinition definition) {
        //设置数据源
        DynamicDataSourceContextHolder.useMasterDataSource();
        super.doBegin(transaction, definition);
    }

    /**
     * 清理本地线程的数据源
     *
     * @param transaction
     */
    @Override
    protected void doCleanupAfterCompletion(Object transaction) {
        super.doCleanupAfterCompletion(transaction);
        DynamicDataSourceContextHolder.clearDataSourceType();
    }

}
