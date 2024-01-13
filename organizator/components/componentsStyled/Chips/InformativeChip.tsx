// @ts-ignore
import styled from "styled-components/native";
import React from "react";

interface InformativeChipProps {
  name: string;
  backgroundColor: string;
  width?: string;
  fontSize?: string;
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

const TagText = styled.Text<{ fontSize: string }>`
  font-weight: bold;
  font-size: ${(props: { fontSize: string }) => props.fontSize || "18px"};
`;

export default function InformativeChip(props: InformativeChipProps) {
  const { name, backgroundColor, width, fontSize } = props;

  return (
    <Chip backgroundColor={backgroundColor} width={width || "auto"}>
      <TagText fontSize={fontSize}>{name}</TagText>
    </Chip>
  );
}
