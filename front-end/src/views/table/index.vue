<template>
  <div class="app-container">
    <el-table
      v-loading="listLoading"
      :data="list.slice((currentPage-1)*pagesize,currentPage*pagesize)"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
    >
      <el-table-column type="expand">
        <template slot-scope="scope">
          <el-form label-position="left" inline class="table-expand">
            <!-- <el-form-item label="Shop Name">
              <span>{{ scope.row.shopName }}</span>
            </el-form-item> -->
            <el-form-item label="Good Comment Ratio">
              <span>{{ scope.row.goodCommentRatio }}</span>
            </el-form-item>
            <el-form-item label="Shop Fans">
              <span>{{ scope.row.numberOfFans }}</span>
            </el-form-item>
            <el-form-item label="Selling Items">
              <span>{{ scope.row.numberOfItems }}</span>
            </el-form-item>
            <el-form-item label="Shop Category">
              <span>{{ scope.row.shopCategory }}</span>
            </el-form-item>
            <el-form-item label="DSR Value">
              <span>{{ scope.row.dsr_value }}</span>
            </el-form-item>
            <el-form-item label="Shop Address">
              <span>{{ scope.row.shopZone }}</span>
            </el-form-item>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column align="center" label="ID" width="95">
        <template slot-scope="scope">
          {{ scope.$index }}
        </template>
      </el-table-column>
      <el-table-column label="ShopName" align="center">
        <template slot-scope="scope">
          {{ scope.row.shopName }}
        </template>
      </el-table-column>
      <el-table-column label="SellerName" width="110" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.sellerName }}</span>
        </template>
      </el-table-column>
      <el-table-column label="WangWang" width="110" align="center">
        <template slot-scope="scope">
          <a :href="scope.row.sellerWangWangURL">
            <img src="@/assets/Wang_icon/wangwang.gif">
          </a>
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="Consumer Insurance" width="95" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.isConsumerInsure | statusFilter">{{ scope.row.isConsumerInsure | firstCharCapitalize }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column align="center" prop="created_at" label="OpeningTime" width="200">
        <template slot-scope="scope">
          <i class="el-icon-time" />
          <span>{{ scope.row.openingDate }}</span>
        </template>
      </el-table-column>
    </el-table>
    <div style="text-align: center;margin-top: 30px;">
      <el-pagination
        background
        layout="prev, pager, next"
        :total="total"
        @current-change="current_change" />
    </div>
  </div>
</template>

<script>
import { getList } from '@/api/table'

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        true: 'success',
        false: 'danger'
      }
      return statusMap[status]
    },
    firstCharCapitalize(word) {
      return word.toString().charAt(0).toUpperCase() + word.toString().slice(1)
    }
  },
  data() {
    return {
      list: [],
      listLoading: true,
      total: 0,
      pagesize: 10,
      currentPage: 1
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      getList().then(response => {
        this.list = response.data
        this.listLoading = false
        this.total = this.list.length
      })
    },
    current_change(currentPage) {
      this.currentPage = currentPage
    }
  }
}
</script>

<style>
  .table-expand {
      font-size: 0;
    }
  .table-expand label {
    width: 190px;
    color: #99a9bf;
  }
  .table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 50%;
  }
</style>
