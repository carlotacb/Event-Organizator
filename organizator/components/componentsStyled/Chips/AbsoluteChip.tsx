// @ts-ignore
import styled from "styled-components/native";
import React from "react";
import InformativeChip from "./InformativeChip";

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

export default function AbsoluteChip(props: StatusChipProps) {
  const { name, backgroundColor } = props;

  return (
    <TagContainer>
      <InformativeChip name={name} backgroundColor={backgroundColor} />
    </TagContainer>
  );
}
