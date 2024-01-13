import React from "react";
import { Text, View } from "react-native";
import FontAwesome from "@expo/vector-icons/FontAwesome";
// @ts-ignore
import styled from "styled-components/native";

const TextError = styled(Text)`
  margin-top: 7px;
  color: red;
  font-size: 12px;
`;

const ErrorIcon = styled(FontAwesome)`
  margin-top: 8px;
  font-size: 12px;
  color: red;
`;

const TextContainerRow = styled(View)`
  display: flex;
  flex-direction: row;
  gap: 5px;
  margin-left: 15px;
  margin-right: 15px;
`;

export default function InputError(props: { error: string | undefined }) {
  const { error } = props;

  return (
    <TextContainerRow>
      <ErrorIcon name="warning" />
      <TextError>{error}</TextError>
    </TextContainerRow>
  );
}
