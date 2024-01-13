// @ts-ignore
import styled from "styled-components/native";
import React from "react";

interface StatusChipProps {
  name: string;
  backgroundColor: string;
}

const TagContainer = styled.View`
  display: flex;
  width: 100%;
  margin-top: 20px;
  align-items: flex-end;
  position: absolute;
  top: -5px;
  right: 15px;
`;

const TagStatus = styled.View<{ backgroundColor: string }>`
  border: 2px solid
    ${(props: { backgroundColor: string }) => props.backgroundColor};
  background-color: ${(props: { backgroundColor: string }) =>
    props.backgroundColor};
  padding: 5px 10px;
  border-radius: 10px;
  text-align: center;
`;

const TagText = styled.Text`
  font-weight: bold;
  font-size: 18px;
`;

export default function AbsoluteChip(props: StatusChipProps) {
  const { name, backgroundColor } = props;

  return (
    <TagContainer>
      <TagStatus backgroundColor={backgroundColor}>
        <TagText>{name}</TagText>
      </TagStatus>
    </TagContainer>
  );
}
