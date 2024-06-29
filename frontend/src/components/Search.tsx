import { useState, useEffect, ChangeEvent } from "react";
import axios from "axios";
import Preview from "./Preview";

export default function Search() {
  const [state, setState] = useState(false);

  const [data, setData] = useState<{ thumbnailLink: string; title: string }[]>(
    []
  );

  const getData = (event: ChangeEvent) => {
    const link = (event.target as HTMLInputElement).value;
    axios
      .get(`http://127.0.0.1:8000/download-video/?url=${link}&resolution=480p`)
      .then((res) => {
        setData(res.data);
      });
  };
  return (
    <>
      <div className="flex flex-row mt-9">
        <div className="basis-1/12" />
        <input
          name="Search"
          type="text"
          maxLength={90}
          className="basis-9/12 border-white"
          placeholder="  Paste Link Here"
          onChange={(event) => getData(event)}
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
      <div>
        {data.length > 0 && (
          <Preview
            thumbnailLink={data[0].thumbnailLink}
            title={data[0].title}
          />
        )}
      </div>
    </>
  );
}
