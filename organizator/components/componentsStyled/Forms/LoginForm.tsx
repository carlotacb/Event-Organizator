import React, { useState } from "react";
import Input from "./Input";
import Button from "../Buttons/ButtonWithIcon";
import { systemColors } from "../tokens";
import { ButtonsRowContainer } from "../Shared/ContainerStyles";
import { handleOnChange, handleError } from "./utilFunctions";

interface LoginInputs {
  username: string;
  password: string;
}

interface LoginFormProps {
  login: () => void;
  inputs: LoginInputs;
  setInputs: React.Dispatch<React.SetStateAction<LoginInputs>>;
}

export default function LoginForm(props: LoginFormProps) {
  const { login, setInputs, inputs } = props;

  const [errors, setErrors] = useState({
    username: undefined,
    password: undefined,
  });

  const validate = () => {
    let isValid = true;

    if (!inputs.username) {
      handleError("Please enter your username", "username", setErrors);
      isValid = false;
    } else {
      handleError(undefined, "username", setErrors);
    }

    if (!inputs.password) {
      handleError("Please enter a password", "password", setErrors);
      isValid = false;
    } else {
      handleError(undefined, "password", setErrors);
    }

    if (isValid) {
      login();
    }
  };

  return (
    <>
      <Input
        label="Username"
        iconName="user"
        value={inputs.username}
        required
        onChangeText={(text) => handleOnChange(text, "username", setInputs)}
        error={errors.username}
      />
      <Input
        label="Password"
        iconName="lock"
        value={inputs.password}
        required
        onChangeText={(text) => handleOnChange(text, "password", setInputs)}
        error={errors.password}
        password
      />
      <ButtonsRowContainer marginTop="30px">
        <Button
          title="Log in"
          onPress={validate}
          iconName="sign-in"
          color={systemColors.accept}
        />
      </ButtonsRowContainer>
    </>
  );
}
