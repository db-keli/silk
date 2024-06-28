import { useState } from "react";

export default function Search() {
  const [state, setState] = useState(false);
  return (
    <div className="flex flex-row mt-5">
      <div className="basis-1/12" />
      <input
        name="Search"
        type="text"
        maxLength={90}
        className="basis-9/12 border-white"
        placeholder="  Paste Link Here"
      />
      <div
        onMouseEnter={() => setState(true)}
        onMouseLeave={() => setState(false)}
        className={
          state === true
            ? "ml-2 basis-1/12 rounded-md"
            : "ml-2 basis-1/12 rounded-md"
        }
      >
        <button
          className={
            state === true
              ? "font-open text-white underline"
              : "font-open text-white"
          }
        >
          Submit
        </button>
      </div>
      <div className="basis-1/12" />
    </div>
  );
}
