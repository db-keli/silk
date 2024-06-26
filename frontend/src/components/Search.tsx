import { useState } from "react";

export default function Search() {
  const [state, setState] = useState(false);
  return (
    <div className="flex flex-row">
      <input
        name="Search"
        type="text"
        maxLength={90}
        className="basis-11/12 border-gray-300"
        placeholder="  Paste Link Here"
      />
      <div
        onMouseEnter={() => setState(true)}
        onMouseLeave={() => setState(false)}
        className={
          state === true
            ? "ml-2 border basis-1/12 bg-red-300 rounded-md"
            : "ml-2 border basis-1/12 rounded-md"
        }
      >
        <text className={state === true ? "font-mono" : "font-sans"}>
          Submit
        </text>
      </div>
    </div>
  );
}
