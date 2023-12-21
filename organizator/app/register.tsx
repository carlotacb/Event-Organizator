import React, { useState } from "react";
import {
  SafeAreaView,
  StyleSheet,
  Text,
  ScrollView,
  ActivityIndicator,
  View,
} from "react-native";

import Input from "../components/Input";
import Button from "../components/StyledButton";

export default function RegisterPage() {
  const [inputs, setInputs] = useState({
    username: "",
    email: "",
    password: "",
    passwordConfirm: "",
    firstName: "",
    lastName: "",
    bio: "",
    // profilePicture: "",
  });
  const [errors, setErrors] = React.useState({
    username: undefined,
    email: undefined,
    password: undefined,
    passwordConfirm: undefined,
    firstName: undefined,
    lastName: undefined,
    bio: undefined,
    // profilePicture: undefined,
  });
  const [loading, setLoading] = React.useState(false);

  const validate = () => {
    let isValid = true;

    if (!inputs.username) {
      handleError("Please enter your username", "username");
      isValid = false;
    } else {
      handleError(undefined, "username");
      isValid = true;
    }

    if (!inputs.email) {
      handleError("Please enter an email address", "email");
      isValid = false;
    } else if (!inputs.email.match(/\S+@\S+\.\S+/)) {
      handleError("Please enter a valid email address", "email");
      isValid = false;
    } else {
      handleError(undefined, "email");
      isValid = true;
    }

    if (!inputs.password) {
      handleError("Please enter a password", "password");
      isValid = false;
    } else if (inputs.password.length < 8) {
      handleError("Minimum password length is 8", "password");
      isValid = false;
    } else {
      handleError(undefined, "password");
      isValid = true;
    }

    if (!inputs.passwordConfirm) {
      handleError("Please enter confirm password", "passwordConfirm");
      isValid = false;
    } else if (inputs.passwordConfirm !== inputs.password) {
      handleError("Password confirmation does not match", "passwordConfirm");
      isValid = false;
    } else {
      handleError(undefined, "passwordConfirm");
      isValid = true;
    }

    if (!inputs.firstName) {
      handleError("Please enter your first name", "firstName");
      isValid = false;
    } else {
      handleError(undefined, "firstName");
      isValid = true;
    }

    if (!inputs.lastName) {
      handleError("Please enter your last name", "lastName");
      isValid = false;
    } else {
      handleError(undefined, "lastName");
      isValid = true;
    }

    if (!inputs.bio) {
      handleError("Please enter your bio", "bio");
      isValid = false;
    } else {
      handleError(undefined, "bio");
      isValid = true;
    }

    /* if (!inputs.profilePicture) {
      handleError("Please enter your profile picture", "profilePicture");
      isValid = false;
    } else {
      handleError(undefined, "profilePicture");
      isValid = true;
    } */

    if (isValid) {
      register();
    }
  };

  const register = () => {
    console.log("register!");
    console.log(inputs);

    setLoading(true);
    setTimeout(() => {
      try {
        setLoading(false);
        console.log("register success!");
      } catch (error) {
        console.log(error);
      }
    }, 3000);
  };

  const handleOnChange = (text: string, input: string) => {
    setInputs((prevState) => ({ ...prevState, [input]: text }));
  };
  const handleError = (text: string | undefined, input: string) => {
    setErrors((prevState) => ({ ...prevState, [input]: text }));
  };

  return (
    <SafeAreaView style={styles.container}>
      {loading ? (
        <View style={{ flex: 1, justifyContent: "center" }}>
          <ActivityIndicator size="large" />
        </View>
      ) : (
        <ScrollView contentContainerStyle={styles.scrollContainer}>
          <Text style={styles.textTitle}>Welcome!</Text>
          <Text style={styles.textSubTitle}>
            We are happy to have you here! Please fill in the following details
          </Text>
          <Input
            label="Username"
            iconName="user"
            required
            onChangeText={(text) => handleOnChange(text, "username")}
            error={errors.username}
          />
          <Input
            label="Email"
            iconName="at"
            required
            onChangeText={(text) => handleOnChange(text, "email")}
            error={errors.email}
            keyboardType="email-address"
          />
          <Input
            label="Password"
            iconName="lock"
            required
            onChangeText={(text) => handleOnChange(text, "password")}
            error={errors.password}
            password
          />
          <Input
            label="Confirm your password"
            required
            iconName="lock"
            onChangeText={(text) => handleOnChange(text, "passwordConfirm")}
            error={errors.passwordConfirm}
            password
          />
          <Input
            label="First Name"
            iconName="id-badge"
            required
            onChangeText={(text) => handleOnChange(text, "firstName")}
            error={errors.firstName}
          />
          <Input
            label="Last Name"
            iconName="id-badge"
            required
            onChangeText={(text) => handleOnChange(text, "lastName")}
            error={errors.lastName}
          />
          <Input
            label="Biography"
            iconName="pencil"
            required
            onChangeText={(text) => handleOnChange(text, "bio")}
            error={errors.bio}
          />
          {/* <Input
            label="Profile Picture"
            iconName="camera"
            required
            onChangeText={(text) => handleOnChange(text, "profilePicture")}
            error={errors.profilePicture}
          /> */}

          <Button title="Register" onPress={validate} />
        </ScrollView>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: "white",
    flex: 1,
  },
  scrollContainer: {
    paddingTop: 30,
    paddingHorizontal: 20,
  },
  textTitle: {
    fontSize: 30,
    fontWeight: "bold",
    color: "black",
  },
  textSubTitle: {
    fontSize: 18,
    color: "black",
    marginVertical: 5,
  },
  image: {
    width: 250,
    height: 250,
    alignSelf: "center",
  },
});
