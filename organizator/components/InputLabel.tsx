import { Text, View } from "react-native";
import React from "react";
// @ts-ignore
import styled from "styled-components/native";

const TextContainerRow = styled(View)`
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

interface TextLabelProps {
  label: string;
  required?: boolean;
}

export default function InputLabel(props: TextLabelProps) {
  const { label, required } = props;

  return (
    <TextContainerRow>
      <TextLabel>{label}</TextLabel>
      <TextRequiredLabel>{required ? "*" : ""}</TextRequiredLabel>
    </TextContainerRow>
  );
}
