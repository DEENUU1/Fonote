import Layout from "@/components/global/Layout";
import {useSession} from "next-auth/react";
import {useEffect, useState} from "react";
import {toast} from "react-toastify";
import {Spinner} from "@chakra-ui/react";
import getListInputData from "@/services/getListInputData";
import getInputDataDetails from "@/services/getInputDataDetails";
import getListResult from "@/services/getListResult";
import SideBar from "@/components/dashboard/SideBar";
import InputDataDetailsRender from "@/components/dashboard/InputDataDetailsRender";
import ResultTypeButtonRender from "@/components/dashboard/ResultTypeButtonRender";
import TranscriptionColumn from "@/components/dashboard/TranscriptionColumn";
import {ResultColumn} from "@/components/dashboard/ResultColumn";
import postResponse from "@/services/postResult";


export default function Dashboard() {
	const {data: session, status} = useSession({required: true});

	const [listInputData, setListInputData] = useState([]);
	const [detailInputData, setDetailInputData] = useState(null);
	const [listResult, setListResult] = useState([]);
	const [isLoading, setIsLoading] = useState(false);
	const [url, setUrl] = useState("");
	const [language, setLanguage] = useState("");
	const [transcription, setTranscription] = useState("");

	const handleSubmitCreateInputData = async (e: any) => {
		e.preventDefault();

		setIsLoading(true);

		const formData = new FormData();
		formData.append("source_url", url);
		formData.append("language", language);
		formData.append("transcription_type", transcription);

		try {
			const response = await fetch(process.env.API_URL + "ai/input/", {
				method: "POST",
				headers: {
					accept: "application/json",
					Authorization: `Bearer ${session?.access_token}`
				},
				body: formData,
			});

			const res = await response.json();

			if (response.ok) {
				toast.success("Input data created successfully");
			} else {
				toast.error(res.detail);
			}
		} catch (error) {
			toast.error("Error while creating Input data object");
		} finally {
			setIsLoading(false);
		}
	};

	useEffect(() => {
		async function fetchData() {
			const data = await getListInputData(session?.access_token);
			setListInputData(data);
		}

		fetchData();
	}, [session?.access_token]);

	const handleListItemClick = async (inputDataId: string) => {
		const detailInputData = await getInputDataDetails(session?.access_token, inputDataId);
		setDetailInputData(detailInputData);

		const listResult = await getListResult(session?.access_token, inputDataId);
		setListResult(listResult);
	};

	const handleResponseCreate = async (inputDataId: string, resultType: string) => {
		if (!detailInputData) {
			toast.error("Input data not found");
			return;
		}


		setIsLoading(true);
		const response = await postResponse(session?.access_token, inputDataId, resultType);

		const listResult = await getListResult(session?.access_token, inputDataId);
		setListResult(listResult);

		setIsLoading(false);
	}

	if (status == "loading") {
		return <Spinner size="lg"/>;
	}

	if (session) {
		return (
			<>
				<Layout>
					<main className={"h-screen"}>
						{
							<>
								<SideBar
									listInputData={listInputData}
									handleListItemClick={handleListItemClick}
									handleSubmitCreateInputData={handleSubmitCreateInputData}
									setUrl={setUrl}
									setLanguage={setLanguage}
									setTranscription={setTranscription}
								/>

								<div className="p-4 sm:ml-64 flex flex-wrap h-[850px]">
									<InputDataDetailsRender detailInputData={detailInputData}/>
									<TranscriptionColumn detailInputData={detailInputData}/>
									<ResultColumn listResult={listResult}/>
									<ResultTypeButtonRender
										handleResponseCreate={handleResponseCreate}
										detailInputData={detailInputData}
										isLoading={isLoading}
									/>
								</div>
							</>
						}
					</main>
				</Layout>
			</>
		);
	}

	return <></>;

}