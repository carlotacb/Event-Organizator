import React from "react";
import { View, Text, TextInput, TextInputProps } from "react-native";
import styled from "styled-components/native";
import FontAwesome from "@expo/vector-icons/FontAwesome";

const Container = styled(View)`
  margin-bottom: 20px;
`;

const LabelInput = styled(View)`
  display: flex;
  flex-direction: row;
  gap: 5px;
`;

const TextLabel = styled(Text)`
  margin-bottom: 8px;
  margin-left: 15px;
`;

const TextRequiredLabel = styled(Text)`
  color: red;
`;

const TextError = styled(Text)`
  margin-top: 7px;
  color: red;
  font-size: 14px;
`;

const TextInputContainer = styled(View)<{ isFocus: boolean }>`
  display: flex;
  flex-direction: row;
  align-items: center;
  background-color: lightcyan;
  height: 55px;
  border-radius: 20px;
  border-width: 1px;
  border-color: ${(props: { isFocus: boolean }) =>
    props.isFocus ? "red" : "blue"};
  padding: 15px;
`;

const InputStyled = styled(TextInput)`
  color: darkblue;
  flex: 1;
  margin-left: 10px;
  outline: none;
`;

const InputIcon = styled(FontAwesome)`
  font-size: 25px;
  color: darkblue;
`;

const EyeIcon = styled(FontAwesome)`
  font-size: 20px;
  color: darkblue;
`;

interface InputProps extends TextInputProps {
  label: string;
  error?: string;
  iconName?: string | never;
  password?: boolean;
  required?: boolean;
}

export default function Input(props: InputProps) {
  const { label, error, required, password, iconName } = props;

  const [hidePassword, setHidePassword] = React.useState(password);
  const [isFocused, setIsFocused] = React.useState(false);

  return (
    <Container>
      <LabelInput>
        <TextLabel>{label}</TextLabel>
        <TextRequiredLabel>{required ? "*" : ""}</TextRequiredLabel>
      </LabelInput>
      <TextInputContainer isFocus={isFocused}>
        {iconName && <InputIcon name={iconName} />}
        <InputStyled
          onFocus={() => {
            setIsFocused(true);
          }}
          onBlur={() => setIsFocused(false)}
          secureTextEntry={hidePassword}
          {...props}
        />
        {password && (
          <EyeIcon
            onPress={() => setHidePassword(!hidePassword)}
            name={hidePassword ? "eye" : "eye-slash"}
          />
        )}
      </TextInputContainer>
      {error && <TextError>{error}</TextError>}
    </Container>
  );
}
