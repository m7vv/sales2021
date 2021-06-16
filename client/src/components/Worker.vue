<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Workers</h1>
        <hr>
        <br><br>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.worker-modal>Add worker</button>
        <br><br>
        <table class="table table-hover">
          <thead>
          <tr>
            <th scope="col">Worker Name</th>
            <th scope="col">Salary</th>
            <th scope="col">Actions</th>
            <th></th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(worker, index) in workers" :key="index">
            <td>{{ worker.name }}</td>
            <td>{{ worker.salary }}</td>
            <td>
              <div class="btn-group" role="group">
                <button
                  type="button"
                  class="btn btn-warning btn-sm"
                  v-b-modal.worker-update-modal
                  @click="editWorker(worker)">
                  Update
                </button>
                <button
                  type="button"
                  class="btn btn-danger btn-sm"
                  @click="onDeleteWorker(worker)">
                  Delete
                </button>
              </div>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addWorkerModal"
             id="worker-modal"
             title="Add a new worker"
             hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-title-group"
                      label="Name of Worker:"
                      label-for="form-name-input">
          <b-form-input id="form-name-input"
                        type="text"
                        v-model="addWorkerForm.name"
                        required
                        placeholder="Enter name of worker">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-salary-group"
                      label="Salary:"
                      label-for="form-salary-input">
          <b-form-input id="form-salary-input"
                        type="text"
                        v-model="addWorkerForm.salary"
                        required
                        placeholder="Enter salary">
          </b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>
    <b-modal ref="editWorkerModal"
             id="worker-update-modal"
             title="Update"
             hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        <b-form-group id="form-title-edit-group"
                      label="Name:"
                      label-for="form-name-edit-input">
          <b-form-input id="form-name-edit-input"
                        type="text"
                        v-model="editForm.name"
                        required
                        placeholder="Enter name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-salary-edit-group"
                      label="Salary:"
                      label-for="form-salary-edit-input">
          <b-form-input id="form-salary-edit-input"
                        type="text"
                        v-model="editForm.salary"
                        required
                        placeholder="Enter salary">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      name: 'Worker',
      workers: [],
      addWorkerForm: {
        name: '',
        salary: '',
      },
      editForm: {
        id: '',
        name: '',
        salary: '',
      },
    };
  },
  methods: {
    getWorkers() {
      const path = 'http://localhost:5000/api/workers/';
      axios.get(path)
        .then((res) => {
          this.workers = res.data;
          console.log(res.data)
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addWorker(payload) {
      const path = 'http://localhost:5000/api/workers';
      axios.post(path, payload)
        .then(() => {
          this.getWorkers();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getWorkers();
        });
    },
    initForm() {
      this.addWorkerForm.name = '';
      this.addWorkerForm.salary = '';
      this.editForm.name = '';
      this.editForm.salary = '';
      this.editForm.uuid = '';

    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addWorkerModal.hide();
      const payload = {
        name: this.addWorkerForm.name,
        salary: this.addWorkerForm.salary,
      };
      this.addWorker(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addWorkerModal.hide();
      this.initForm();
    },
    editWorker(worker) {
      this.editForm = worker;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editWorkerModal.hide();
      const payload = {
        name: this.editForm.name,
        salary: this.editForm.salary,

      };
      this.updateWorker(payload, this.editForm.uuid);
    },
    updateWorker(payload, workerUUID) {
      const path = `http://localhost:5000/api/workers/${workerUUID}`;
      axios.put(path, payload)
        .then(() => {
          this.getWorkers();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getWorkers();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editWorkerModal.hide();
      this.initForm();
      this.getWorkers();
    },
    removeWorker(workerUUID) {
      const path = `http://localhost:5000/api/workers/${workerUUID}`;
      axios.delete(path)
        .then(() => {
          this.getWorkers();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getWorkers();
        });
    },
    onDeleteWorker(worker) {
      this.removeWorker(worker.uuid);
    },
  },
  created() {
    this.getWorkers();
  },
};
</script>

<style scoped>

</style>
