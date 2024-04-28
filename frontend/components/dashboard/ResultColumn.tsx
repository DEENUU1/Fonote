import {Chip} from "@nextui-org/react";
import MarkdownRenderer from "@/components/global/MarkdownRenderer";


export function ResultColumn(
	{
		listResult
	}:
	{
		listResult: any
	}
){

	return (
		<>
			<div
				className="p-4 w-1/2 border-2 flex-grow border-gray-200 border-solid rounded-lg dark:border-gray-700 overflow-y-auto"
				style={{maxHeight: "850px"}}>
				{Array.isArray(listResult) && (listResult.length > 0 && (
					listResult?.map((result) => (
						<li key={result?.id} className={"mb-5 list-none"}>
							<div>
								<Chip color={"default"} variant={"bordered"}>{result?.result_type}</Chip>
								<MarkdownRenderer markdown={result?.content}/>
							</div>
						</li>
					))
				))}
			</div>
		</>
	)
}