<template>
  <div class="app-container">
    <el-form ref="form" :model="form" label-width="90px">
      <el-form-item label="Username" style="width:30%;display:inline-block;">
        <el-input v-model="form.username" />
      </el-form-item>
      <el-form-item label="Password" style="width:30%;display:inline-block;">
        <el-input v-model="form.password" show-password />
      </el-form-item>
      <el-form-item style="display:inline-block;" label-width="0px">
        <el-button-group>
          <el-button type="primary" style="margin-left:20px" @click="onAdd">Addin</el-button>
          <el-button type="danger" @click="onClear">Clear</el-button>
        </el-button-group>
      </el-form-item>
    </el-form>

    <el-form>
      <div id="controllButton" style="margin-bottom:10px">
        <div v-if="runningPromises" style="float:left;">
          <el-button type="danger" @click="stopCollect">Stop</el-button>
        </div>
        <div v-else style="float:left">
          <el-button type="primary" @click="startCollect">Start</el-button>
        </div>
        <el-tag type="info" style="line-height:40px;height:38px;float:right;">Select the accounts and click Start button to start collect shops.</el-tag>
      </div>
      <el-table
        v-loading="accountsLoading"
        :data="accounts"
        element-loading-text="Loading"
        border
        fit
        highlight-current-row
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column align="center" label="ID" width="95">
          <template slot-scope="scope">
            {{ scope.$index }}
          </template>
        </el-table-column>
        <el-table-column label="Username">
          <template slot-scope="scope">
            {{ scope.row.username }}
          </template>
        </el-table-column>
        <el-table-column label="Account status" width="125" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status | statusFilter">{{ scope.row.status | statusTextDisplay }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="Modify" width="140" align="center">
          <template scope="scope">
            <el-button @click="onEditForm(scope.$index, scope.row)">Modify Info</el-button>
          </template>
        </el-table-column>
        <el-table-column class-name="status-col" label="Delete" width="110" align="center">
          <template scope="scope">
            <el-button type="danger" @click="onDelete(scope.$index, scope.row)">Delete</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-form>

    <el-dialog
      title="EditKanDianBaoAcount"
      :visible.sync="editorVisible"
      width="30%"
      :before-close="handleClose"
    >
      <el-form ref="editForm" :model="editForm" label-width="82px">
        <el-form-item label="Username" style="margin-right=20px">
          <el-input v-model="editForm.username" disabled />
        </el-form-item>
        <el-form-item label="Password" style="margin-right=20px">
          <el-input v-model="editForm.password" show-password />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editorVisible = false">Cancel</el-button>
        <el-button type="primary" @click="onEditSubmit">Modify</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { getKdbAccounts, putKdbAccounts, delKdbAccounts, addKdbAccounts, beginKdbCollect, stopKdbCollect } from '@/api/kdbaccount'
export default {
  data() {
    return {
      form: {
        username: '',
        password: ''
      },
      editForm: {
        username: '',
        password: ''
      },
      accounts: null,
      accountsLoading: true,
      editorVisible: false,
      multipleSelections: [],
      runningPromises: 0
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    onSubmit() {
      this.$message('submit!')
    },
    onCancel() {
      this.$message({
        message: 'cancel!',
        type: 'warning'
      })
    },
    fetchData() {
      this.accountsLoading = true
      getKdbAccounts().then(response => {
        this.accounts = response.data
        this.accountsLoading = false
        // this.$set(this.accounts[0], 'status', 1)
        for (var i = 0; i < this.accounts.length; i++) {
          this.$set(this.accounts[i], 'status', 0)
        }
      })
    },
    handleClose(done) {
      this.$confirm('Close editor window?')
        .then(_ => {
          done()
        })
        .catch(_ => {})
    },
    onEditForm(index, row) {
      this.editorVisible = true
      this.editForm = Object.assign({}, row)
    },
    onEditSubmit() {
      const data = {
        'username': this.editForm.username,
        'password': this.editForm.password
      }
      putKdbAccounts(data).then(response => {
        this.editorVisible = false
        this.fetchData()
        this.$message({
          message: 'Account ' + data.username + ' edited!',
          type: 'success'
        })
      }).catch((error) => {
        console.error(error)
      })
    },
    onDelete(index, row) {
      const data = {
        'username': Object.assign({}, row).username
      }
      delKdbAccounts(data).then(response => {
        this.fetchData()
        this.$message({
          message: 'Account ' + data.username + ' deleted!',
          type: 'success'
        })
      }).catch((error) => {
        console.error(error)
      })
    },
    onAdd() {
      const data = {
        'username': this.form.username,
        'password': this.form.password
      }
      this.form.username = ''
      this.form.password = ''
      addKdbAccounts(data).then(response => {
        this.fetchData()
        this.$message({
          message: 'Account ' + data.username + ' added!',
          type: 'success'
        })
      }).catch((error) => {
        console.error(error)
      })
    },
    onClear() {
      this.form.username = ''
      this.form.password = ''
    },
    handleSelectionChange(val) {
      this.multipleSelections = val
    },
    startCollect() {
      if (this.multipleSelections.length === 0) {
        this.$notify.error({
          title: 'Failed',
          message: 'You need to select the account to collect'
        })
        return
      }
      this.$notify.warning({
        title: 'Collecting',
        message: 'Don\'t switch the page!'
      })
      this.multipleSelections.forEach(acc => {
        this.$set(this, 'runningPromises', this.runningPromises + 1)
        acc.status = 2 // waiting
        beginKdbCollect(acc.username).then(response => {
          acc.status = 3 // success
          this.$message.success({
            title: 'Complete',
            message: '限额已耗尽: ' + acc.username
          })
          this.$set(this, 'runningPromises', this.runningPromises - 1)
        }).catch(error => {
          acc.status = 4 // fail
          console.error(error)
          // this.$notify.error({
          //   title: 'Failed',
          //   message: 'Errors with account: ' + acc.username
          // })
          this.$set(this, 'runningPromises', this.runningPromises - 1)
        })
      })
    },
    stopCollect() {
      this.multipleSelections.forEach(acc => {
        stopKdbCollect(acc.username).then(response => {
          this.$notify.success({
            title: 'Stopped',
            message: 'Successfully stopped'
          })
        }).catch(error => {
          console.error(error)
        })
      })
    }
  },
  filters: {
    statusFilter(status) {
      const statusMap = {
        0: 'info',
        1: 'primary',
        2: 'warning',
        3: 'success',
        4: 'danger'
      }
      return statusMap[status]
    },
    statusTextDisplay(status) {
      const statusMap = {
        0: 'Not Running',
        1: 'Running',
        2: 'Waiting',
        3: 'Successed',
        4: 'Failed'
      }
      return statusMap[status]
    },
    controllBtn(status) {
      const statusMap = {
        true: 'Stop',
        false: 'Start'
      }
      return statusMap[status]
    }
  }
}
</script>

<style scoped>
.line{
  text-align: center;
}
</style>
