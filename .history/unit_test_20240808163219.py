

reply = getType(msg)
        result = json.loads(reply)
        tasks_id = result.get('tasks_id')
        cateogry = result.get('cateogry')