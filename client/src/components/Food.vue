<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Foods</h1>
        <hr>
        <br><br>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.food-modal>Add food</button>
        <br><br>
        <table class="table table-hover">
          <thead>
          <tr>
            <th scope="col">Food Name</th>
            <th scope="col">Price</th>
            <th scope="col">Actions</th>
            <th></th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(food, index) in foods" :key="index">
            <td>{{ food.name }}</td>
            <td>{{ food.price }}</td>
            <td>
              <div class="btn-group" role="group">
                <button
                  type="button"
                  class="btn btn-warning btn-sm"
                  v-b-modal.food-update-modal
                  @click="editFood(food)">
                  Update
                </button>
                <button
                  type="button"
                  class="btn btn-danger btn-sm"
                  @click="onDeleteFood(food)">
                  Delete
                </button>
              </div>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addFoodModal"
             id="food-modal"
             title="Add a new food"
             hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-title-group"
                      label="Name of Food:"
                      label-for="form-name-input">
          <b-form-input id="form-name-input"
                        type="text"
                        v-model="addFoodForm.name"
                        required
                        placeholder="Enter name of food">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-price-group"
                      label="Price:"
                      label-for="form-price-input">
          <b-form-input id="form-price-input"
                        type="text"
                        v-model="addFoodForm.price"
                        required
                        placeholder="Enter price">
          </b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>
    <b-modal ref="editFoodModal"
             id="food-update-modal"
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
        <b-form-group id="form-price-edit-group"
                      label="Price:"
                      label-for="form-price-edit-input">
          <b-form-input id="form-price-edit-input"
                        type="text"
                        v-model="editForm.price"
                        required
                        placeholder="Enter price">
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
      name: 'Food',
      foods: [],
      addFoodForm: {
        name: '',
        price: '',
      },
      editForm: {
        id: '',
        name: '',
        price: '',
      },
    };
  },
  methods: {
    getFoods() {
      const path = 'http://localhost:5000/api/foods/';
      axios.get(path)
        .then((res) => {
          this.foods = res.data;
          console.log(res.data)
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addFood(payload) {
      const path = 'http://localhost:5000/api/foods';
      axios.post(path, payload)
        .then(() => {
          this.getFoods();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getFoods();
        });
    },
    initForm() {
      this.addFoodForm.name = '';
      this.addFoodForm.price = '';
      this.editForm.name = '';
      this.editForm.price = '';
      this.editForm.uuid = '';

    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addFoodModal.hide();
      const payload = {
        name: this.addFoodForm.name,
        price: this.addFoodForm.price,
      };
      this.addFood(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addFoodModal.hide();
      this.initForm();
    },
    editFood(food) {
      this.editForm = food;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editFoodModal.hide();
      const payload = {
        name: this.editForm.name,
        price: this.editForm.price,

      };
      this.updateFood(payload, this.editForm.uuid);
    },
    updateFood(payload, foodUUID) {
      const path = `http://localhost:5000/api/foods/${foodUUID}`;
      axios.put(path, payload)
        .then(() => {
          this.getFoods();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getFoods();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editFoodModal.hide();
      this.initForm();
      this.getFoods();
    },
    removeFood(foodUUID) {
      const path = `http://localhost:5000/api/foods/${foodUUID}`;
      axios.delete(path)
        .then(() => {
          this.getFoods();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getFoods();
        });
    },
    onDeleteFood(food) {
      this.removeFood(food.uuid);
    },
  },
  created() {
    this.getFoods();
  },
};
</script>

<style scoped>

</style>
