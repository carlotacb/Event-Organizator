import React from "react";
import { View, TextInput, TextInputProps, Platform } from "react-native";
// @ts-ignore
import styled from "styled-components/native";
import FontAwesome from "@expo/vector-icons/FontAwesome";
import InputLabel from "./InputLabel";
import InputError from "./InputError";

const Container = styled(View)<{ width: string }>`
  margin-bottom: 20px;
  width: ${(props: { width: string }) => props.width};
`;

const TextInputContainer = styled(View)<{
  isFocus: boolean;
  disabled: boolean;
}>`
  display: flex;
  flex-direction: row;
  align-items: center;
  background-color: ${(props: { isFocus: boolean; disabled: boolean }) =>
    props.isFocus ? "transparent" : props.disabled ? "#969696" : "#eaeaea"};
  border-radius: 15px;
  border-width: 2px;
  border-color: ${(props: { isFocus: boolean }) =>
    props.isFocus ? "#a9a9a9" : "#eaeaea"};
  padding: 3px 20px;
`;

const InputStyled = styled(TextInput)<{
  disabled: boolean;
}>`
  color: ${(props: { disabled: boolean }) =>
    props.disabled ? "#eaeaea" : "black"};
  flex: 1;
  margin-left: 10px;
  margin-right: 10px;
`;

const InputIcon = styled(FontAwesome)<{
  disabled: boolean;
}>`
  font-size: 20px;
  color: ${(props: { disabled: boolean }) =>
    props.disabled ? "#eaeaea" : "dimgray"};
`;

const EyeIcon = styled(FontAwesome)`
  font-size: 15px;
  color: darkslategray;
`;

interface InputProps extends TextInputProps {
  label?: string;
  error?: string;
  iconName?: string | never;
  password?: boolean;
  required?: boolean;
  disabled?: boolean;
  width?: string;
}

export default function Input(props: InputProps) {
  const {
    label,
    error,
    required,
    password,
    iconName,
    disabled,
    width = "auto",
  } = props;

  const [hidePassword, setHidePassword] = React.useState(password);
  const [isFocused, setIsFocused] = React.useState(false);

  return (
    <Container width={width}>
      {disabled && !label ? null : (
        <InputLabel label={label || ""} required={required} />
      )}
      <TextInputContainer isFocus={isFocused} error={error} disabled={disabled}>
        {iconName && <InputIcon name={iconName} disabled={disabled} />}
        <InputStyled
          disabled={disabled}
          style={[
            Platform.OS === "web"
              ? { outlineStyle: "none", padding: 10 }
              : { padding: 10 },
          ]}
          onFocus={() => {
            if (!disabled) setIsFocused(true);
          }}
          onBlur={() => {
            if (!disabled) setIsFocused(false);
          }}
          secureTextEntry={hidePassword}
          editable={!disabled}
          {...props}
        />
        {password && (
          <EyeIcon
            onPress={() => setHidePassword(!hidePassword)}
            name={hidePassword ? "eye" : "eye-slash"}
          />
        )}
      </TextInputContainer>
      {error && <InputError error={error} />}
    </Container>
  );
}
