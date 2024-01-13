// @ts-ignore
import styled from "styled-components/native";
import React from "react";

interface InformativeChipProps {
  name: string;
  backgroundColor: string;
  width?: string;
}

const Chip = styled.View<{ backgroundColor: string }>`
  border: 2px solid
    ${(props: { backgroundColor: string }) => props.backgroundColor};
  background-color: ${(props: { backgroundColor: string }) =>
    props.backgroundColor};
  padding: 5px 10px;
  border-radius: 20px;
  text-align: center;
`;

const TagText = styled.Text`
  font-weight: bold;
  font-size: 18px;
`;

export default function InformativeChip(props: InformativeChipProps) {
  const { name, backgroundColor, width } = props;

  return (
    <Chip backgroundColor={backgroundColor} width={width || "auto"}>
      <TagText>{name}</TagText>
    </Chip>
  );
}
