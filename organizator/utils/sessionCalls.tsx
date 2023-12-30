import AsyncStorage from "@react-native-async-storage/async-storage";

export const storeToken = async (value: string) => {
  await AsyncStorage.setItem("session-token", value);
};

export const getToken = (): Promise<string | null> =>
  AsyncStorage.getItem("session-token");

export const removeToken = async () => {
  await AsyncStorage.removeItem("session-token");
};
