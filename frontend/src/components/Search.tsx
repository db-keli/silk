import { useState, ChangeEvent } from "react";
import axios from "axios";
import Preview from "./Preview";

export default function Search() {
  const [state, setState] = useState(false);
  const [loading, setLoading] = useState(false);
  const [download, setDownload] = useState(false);
  const [data, setData] = useState<{ thumbnailLink: string; title: string }[]>(
    []
  );

  const getData = async (event: ChangeEvent) => {
    setLoading(true);
    const link = (event.target as HTMLInputElement).value;
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/download-video/?url=${link}&resolution=480p`
      );
      const data = response.data.data;
      setData(data);
      console.log(String(data));
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const getDataOnMouseClick = async () => {
    setLoading(true);
    const link = document.querySelector("input")?.value;
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/download-video/?url=${link}&resolution=480p`
      );
      const data = response.data.data;
      setData(data);
      console.log(String(data));
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="flex flex-row mt-20">
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
            onClick={getDataOnMouseClick}
          >
            Submit
          </button>
        </div>
        <div className="basis-1/12" />
      </div>
      {loading && (
        <div className=" justify-center text-center mt-2 font-open text-white loader">
          Loading......
        </div>
      )}
      <div>
        {loading === false && data.length > 0 && (
          <Preview thumbnailLink={String(data[1])} title={String(data[0])} />
        )}
      </div>
      <div className="flex flex-row mt-20">
        <div className="basis-1/12" />
        <button
          className={
            download === true
              ? "basis-9/12 bg-cyan-600 rounded-md font-open text-white font-bold text-center w-full"
              : "basis-9/12 rounded-md font-open text-white font-bold text-center w-full"
          }
          onMouseEnter={() => setDownload(true)}
          onMouseLeave={() => setDownload(false)}
        >
          download
        </button>
        <div className="basis-2/12" />
      </div>
    </>
  );
}
