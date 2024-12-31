export const State = {
    data: {},
    set(key, value) {
        this.data[key] = value;
        console.log(`State updated: ${key} = ${value}`);
    },
    get(key) {
        return this.data[key];
    }
};